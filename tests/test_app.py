import unittest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.app import app
from server.seed import seed_database


class AppIntegrationTests(unittest.TestCase):
    def setUp(self):
        seed_database()
        self.client = app.test_client()

    def test_list_endpoints(self):
        self.assertEqual(self.client.get('/workouts').status_code, 200)
        self.assertEqual(self.client.get('/exercises').status_code, 200)

    def test_create_and_delete_workout_and_exercise(self):
        exercise_resp = self.client.post('/exercises', json={
            'name': 'Burpee',
            'category': 'Full Body',
            'equipment_needed': False,
        })
        self.assertEqual(exercise_resp.status_code, 201)
        exercise_id = exercise_resp.json['id']

        workout_resp = self.client.post('/workouts', json={
            'date': '2026-07-26',
            'duration_minutes': 30,
            'notes': 'Test workout',
        })
        self.assertEqual(workout_resp.status_code, 201)
        workout_id = workout_resp.json['id']

        assoc_resp = self.client.post(
            f'/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises',
            json={'reps': 10, 'sets': 3},
        )
        self.assertEqual(assoc_resp.status_code, 201)
        self.assertEqual(assoc_resp.json['workout_id'], workout_id)
        self.assertEqual(assoc_resp.json['exercise_id'], exercise_id)

        self.assertEqual(self.client.get(f'/workouts/{workout_id}').status_code, 200)
        self.assertEqual(self.client.get(f'/exercises/{exercise_id}').status_code, 200)

        self.assertEqual(self.client.delete(f'/exercises/{exercise_id}').status_code, 200)
        self.assertEqual(self.client.delete(f'/workouts/{workout_id}').status_code, 200)

    def test_duplicate_workout_exercise_assignment(self):
        exercise_resp = self.client.post('/exercises', json={
            'name': 'Sit-up',
            'category': 'Core',
            'equipment_needed': False,
        })
        workout_resp = self.client.post('/workouts', json={
            'date': '2026-07-26',
            'duration_minutes': 20,
            'notes': 'Duplicate test',
        })
        exercise_id = exercise_resp.json['id']
        workout_id = workout_resp.json['id']

        first = self.client.post(
            f'/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises',
            json={'reps': 12, 'sets': 2},
        )
        self.assertEqual(first.status_code, 201)

        duplicate = self.client.post(
            f'/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises',
            json={'reps': 8, 'sets': 2},
        )
        self.assertEqual(duplicate.status_code, 400)

    def test_invalid_payloads(self):
        missing_date = self.client.post('/workouts', json={'duration_minutes': 15})
        self.assertEqual(missing_date.status_code, 400)

        missing_name = self.client.post('/exercises', json={'category': 'Strength', 'equipment_needed': False})
        self.assertEqual(missing_name.status_code, 400)

        bad_assoc = self.client.post('/workouts/1/exercises/1/workout_exercises', json={'reps': 10})
        self.assertEqual(bad_assoc.status_code, 400)


if __name__ == '__main__':
    unittest.main()
