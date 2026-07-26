from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code


@app.route('/workouts', methods=['GET'])
def list_workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return error_response('Workout not found', 404)
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    payload = request.get_json() or {}
    try:
        workout_data = workout_schema.load(payload)
        workout = Workout(**workout_data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as exc:
        return error_response(exc.messages, 400)
    except (ValueError, IntegrityError) as exc:
        db.session.rollback()
        return error_response(str(exc), 400)


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return error_response('Workout not found', 404)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': f'Workout {workout_id} deleted'}), 200


@app.route('/exercises', methods=['GET'])
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return error_response('Exercise not found', 404)
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    payload = request.get_json() or {}
    try:
        exercise_data = exercise_schema.load(payload)
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except ValidationError as exc:
        return error_response(exc.messages, 400)
    except (ValueError, IntegrityError) as exc:
        db.session.rollback()
        return error_response(str(exc), 400)


@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return error_response('Exercise not found', 404)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': f'Exercise {exercise_id} deleted'}), 200


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return error_response('Workout not found', 404)
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return error_response('Exercise not found', 404)

    payload = request.get_json() or {}
    payload['workout_id'] = workout_id
    payload['exercise_id'] = exercise_id
    try:
        association_data = workout_exercise_schema.load(payload)
        workout_exercise = WorkoutExercise(**association_data)
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except ValidationError as exc:
        return error_response(exc.messages, 400)
    except (ValueError, IntegrityError) as exc:
        db.session.rollback()
        return error_response(str(exc), 400)


if __name__ == '__main__':
    app.run(debug=True, port=5555)
