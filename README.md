# workout-backend-api
# Workout API Backend

## Project Description

This project is a Flask-based REST API for a workout tracking application used by personal trainers. It allows users to create and manage workouts and exercises, and associate multiple exercises with workouts through a many-to-many relationship. The system uses Flask, SQLAlchemy, and Marshmallow to handle database models, serialization, validation, and API routing.

The API is designed with proper database constraints, model validations, and schema validations to ensure data integrity and consistency.

---

## Features

- Create, view, and delete workouts
- Create, view, and delete exercises
- Associate exercises with workouts (many-to-many relationship)
- Store reps, sets, and duration per workout-exercise relationship
- Input validation at model and schema level
- Database constraints to enforce data integrity

---

## Technologies Used

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd workout-backend-api

2. Create virtual environment and install dependencies
pipenv install
pipenv shell
3. Run database migrations
flask db init
flask db migrate -m "initial migration"
flask db upgrade
4. Seed the database
python server/seed.py
Running the Application
python server/app.py

The server will run at:

http://127.0.0.1:5555

** API Endpoints

## Workouts
GET /workouts

Returns all workouts.

GET /workouts/<id>

Returns a single workout and its associated exercises.

POST /workouts

Creates a new workout.

Request body:

{
  "date": "2026-04-22",
  "duration_minutes": 60,
  "notes": "Leg day"
}
DELETE /workouts/<id>

Deletes a workout.

## Exercises
GET /exercises

Returns all exercises.

GET /exercises/<id>

Returns a single exercise and associated workouts.

POST /exercises

Creates a new exercise.

Request body:

{
  "name": "Squat",
  "category": "strength",
  "equipment_needed": true
}
DELETE /exercises/<id>

Deletes an exercise.

- # Workout Exercises (Relationship)
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Links an exercise to a workout with performance data.

Request body:

{
  "reps": 10,
  "sets": 3,
  "duration_seconds": 0
}

#Data Model Summary

## Workout
id (primary key)
date
duration_minutes
notes

## Exercise
id (primary key)
name
category
equipment_needed

## WorkoutExercise (Join Table)
id (primary key)
workout_id (foreign key)
exercise_id (foreign key)
reps
sets
duration_seconds
** 

## Validations
- Model Level
Exercise name must be at least 2 characters
Duration must be greater than 0
Reps and sets must be greater than 0
Exercise category must be valid

- Schema Level
Required fields enforced
Category restricted to valid values
Numeric range validation applied
- Database Constraints
Unique constraint on workout_id and exercise_id
Foreign key relationships enforced
Check constraints for positive values

- Git Workflow
Feature-based branching used
Meaningful commit messages included
Final working branch: endpoints

