from datetime import date

from .app import app
from .models import db, Exercise, Workout, WorkoutExercise



def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        push_up = Exercise(name='Push-up', category='Strength', equipment_needed=False)
        squat = Exercise(name='Squat', category='Strength', equipment_needed=False)
        plank = Exercise(name='Plank', category='Core', equipment_needed=False)
        cycling = Exercise(name='Stationary Bike', category='Cardio', equipment_needed=True)

        morning_workout = Workout(
            date=date.today(),
            duration_minutes=40,
            notes='Morning strength and endurance session.'
        )
        evening_workout = Workout(
            date=date.today(),
            duration_minutes=25,
            notes='Quick cardio and core focus.'
        )

        db.session.add_all([push_up, squat, plank, cycling, morning_workout, evening_workout])
        db.session.commit()

        session1 = WorkoutExercise(workout=morning_workout, exercise=push_up, reps=12, sets=3)
        session2 = WorkoutExercise(workout=morning_workout, exercise=squat, reps=15, sets=3)
        session3 = WorkoutExercise(workout=evening_workout, exercise=plank, duration_seconds=90)
        session4 = WorkoutExercise(workout=evening_workout, exercise=cycling, duration_seconds=1200)

        db.session.add_all([session1, session2, session3, session4])
        db.session.commit()

        print('Seed data created successfully.')


if __name__ == '__main__':
    seed_database()
