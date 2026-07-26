import unittest
from datetime import date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import WorkoutExerciseSchema


class ModelValidationTests(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_exercise_non_empty_name(self):
        with app.app_context():
            with self.assertRaises(ValueError):
                exercise = Exercise(name='', category='Strength', equipment_needed=False)
                db.session.add(exercise)
                db.session.commit()

    def test_workout_date_validation(self):
        with app.app_context():
            with self.assertRaises(ValueError):
                workout = Workout(date='2026-07-26', duration_minutes=20)
                db.session.add(workout)
                db.session.commit()

    def test_workout_exercise_schema_requires_reps_sets_or_duration(self):
        schema = WorkoutExerciseSchema()
        with self.assertRaises(Exception):
            schema.load({'workout_id': 1, 'exercise_id': 1, 'reps': 10})

    def test_workout_exercise_reps_sets_consistency(self):
        with app.app_context():
            exercise = Exercise(name='Burpee', category='Full Body', equipment_needed=False)
            workout = Workout(date=date(2026, 7, 26), duration_minutes=20)
            db.session.add_all([exercise, workout])
            db.session.commit()
            with self.assertRaises(ValueError):
                assoc = WorkoutExercise(workout_id=workout.id, exercise_id=exercise.id, reps=10)
                db.session.add(assoc)
                db.session.commit()


if __name__ == '__main__':
    unittest.main()
