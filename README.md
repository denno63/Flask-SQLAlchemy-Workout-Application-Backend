# Workout Tracker Backend API

A Flask backend API for managing workouts, exercises, and workout exercise assignments. This project uses Flask, SQLAlchemy, Flask-Migrate, and Marshmallow to provide a validated REST API for personal trainers.

## Features

- Create, list, view, and delete workouts
- Create, list, view, and delete exercises
- Add exercises to workouts with reps/sets or duration
- Validations at the database, model, and schema layers
- Automatic serialization and relationship nesting via Marshmallow

## Installation

1. Install dependencies using Pipenv:

```bash
pipenv install
```

2. Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

1. Set the Flask application path:

```bash
export FLASK_APP=wsgi
```

2. Initialize migrations:

```bash
flask db init
```

3. Generate the initial migration:

```bash
flask db migrate -m "Initial workout exercise models"
```

4. Apply the migration:

```bash
flask db upgrade
```

## Seed Data

Populate the database with starter data:

```bash
pipenv run python -m server.seed
```

## Run the Application

Start the Flask server:

```bash
export FLASK_APP=wsgi
flask run --port 5555
```

## Seed Reset

The seed file will reset the database before inserting starter data. Run it again to reset the local data:

```bash
pipenv run python -m server.seed
```

## Tests

Run the automated test suite:

```bash
pipenv run python -m unittest discover -s tests
```

## API Endpoints

### Workouts

- `GET /workouts`
  - List all workouts
- `GET /workouts/<id>`
  - Retrieve a workout and its related exercises
- `POST /workouts`
  - Create a new workout
  - JSON body example:
    ```json
    {
      "date": "2026-07-26",
      "duration_minutes": 45,
      "notes": "Strength and conditioning"
    }
    ```
- `DELETE /workouts/<id>`
  - Delete a workout

### Exercises

- `GET /exercises`
  - List all exercises
- `GET /exercises/<id>`
  - Retrieve an exercise and its related workouts
- `POST /exercises`
  - Create a new exercise
  - JSON body example:
    ```json
    {
      "name": "Push-up",
      "category": "Strength",
      "equipment_needed": false
    }
    ```
- `DELETE /exercises/<id>`
  - Delete an exercise

### Workout Exercise Assignments

- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
  - Add an exercise to a workout
  - JSON body example using reps/sets:
    ```json
    {
      "reps": 12,
      "sets": 3
    }
    ```
  - JSON body example using duration:
    ```json
    {
      "duration_seconds": 90
    }
    ```

## Validation Rules

- Exercise `name` and `category` must be non-empty strings
- Workout `duration_minutes` must be a non-negative integer
- Workout exercises must provide either `duration_seconds` or both `reps` and `sets`
- Duplicate exercise assignments for the same workout are prevented

## Project Structure

- `server/app.py` - Flask application and endpoint definitions
- `server/models.py` - SQLAlchemy model definitions and validations
- `server/schemas.py` - Marshmallow schemas and request validation
- `server/seed.py` - Seed script to populate the database
- `migrations/` - Flask-Migrate migration files

## Notes

- The project uses SQLite for local development in `app.db`
- The `server` package is the primary application package
- No update endpoints are implemented by design
