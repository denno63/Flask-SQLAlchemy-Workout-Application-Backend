from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=0))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))
    exercise = fields.Nested('ExerciseSchema', only=('id', 'name', 'category', 'equipment_needed'), dump_only=True)
    workout = fields.Nested('WorkoutSchema', only=('id', 'date', 'duration_minutes', 'notes'), dump_only=True)

    @validates_schema
    def validate_activity_details(self, data, **kwargs):
        reps = data.get('reps')
        sets = data.get('sets')
        duration_seconds = data.get('duration_seconds')

        if duration_seconds is None and (reps is None or sets is None):
            raise ValidationError('WorkoutExercise requires either duration_seconds or both reps and sets')
        if (reps is None) != (sets is None):
            raise ValidationError('Both reps and sets must be provided together or omitted together')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=0))
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, exclude=('workout',), dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True, validate=validate.Length(min=1))
    equipment_needed = fields.Bool(required=True)
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, exclude=('exercise',), dump_only=True)
