from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import db, Exercise, Workout, WorkoutExercise
from .schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

