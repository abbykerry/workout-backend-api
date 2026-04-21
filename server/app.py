from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from datetime import datetime
import os

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


@app.route('/')
def home():
    return make_response(jsonify({"message": "Workout API running"}), 200)


# ---------------- WORKOUT ROUTES ----------------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()

        new_workout = Workout(
            date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )

        db.session.add(new_workout)
        db.session.commit()

        return make_response(workout_schema.dump(new_workout), 201)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response(jsonify({"message": "Workout deleted"}), 200)


# ---------------- EXERCISE ROUTES ----------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()

        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )

        db.session.add(new_exercise)
        db.session.commit()

        return make_response(exercise_schema.dump(new_exercise), 201)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()

    return make_response(jsonify({"message": "Exercise deleted"}), 200)


# ---------------- WORKOUT-EXERCISE LINK ROUTE ----------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        workout = Workout.query.get(workout_id)
        exercise = Exercise.query.get(exercise_id)

        if not workout or not exercise:
            return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

        data = request.get_json()

        new_link = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data['reps'],
            sets=data['sets'],
            duration_seconds=data.get('duration_seconds')
        )

        db.session.add(new_link)
        db.session.commit()

        return make_response(workout_exercise_schema.dump(new_link), 201)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)