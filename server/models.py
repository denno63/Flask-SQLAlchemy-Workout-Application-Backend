from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, event
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    category = db.Column(db.String(128), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan', passive_deletes=True
    )
    workouts = db.relationship(
        'Workout', secondary='workout_exercise', back_populates='exercises', viewonly=True
    )

    @validates('name', 'category')
    def validate_non_empty(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} must be a non-empty string')
        return value.strip()

class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan', passive_deletes=True
    )
    exercises = db.relationship(
        'Exercise', secondary='workout_exercise', back_populates='workouts', viewonly=True
    )

    __table_args__ = (
        CheckConstraint('duration_minutes >= 0', name='check_workout_duration_non_negative'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or not isinstance(value, int) or value < 0:
            raise ValueError('duration_minutes must be a non-negative integer')
        return value

    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError('date must be a valid date object')
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        CheckConstraint('(reps IS NULL OR reps >= 0)', name='check_reps_non_negative'),
        CheckConstraint('(sets IS NULL OR sets >= 0)', name='check_sets_non_negative'),
        CheckConstraint('(duration_seconds IS NULL OR duration_seconds >= 0)', name='check_duration_seconds_non_negative'),
        UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise_assignment'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_quantity(self, key, value):
        if value is None:
            return None
        if not isinstance(value, int) or value < 0:
            raise ValueError(f'{key} must be a non-negative integer')
        return value


@event.listens_for(WorkoutExercise, 'before_insert')
@event.listens_for(WorkoutExercise, 'before_update')
def validate_workout_exercise(mapper, connection, target):
    if target.duration_seconds is None:
        if target.reps is None or target.sets is None:
            raise ValueError('WorkoutExercise must include either duration_seconds or both reps and sets')
    if (target.reps is None) != (target.sets is None):
        raise ValueError('Both reps and sets must be provided together or omitted together')
