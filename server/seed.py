#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    print("Clearing database...")

    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()

    db.session.commit()

    print("Creating exercises...")

    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    run = Exercise(name="Running", category="cardio", equipment_needed=False)
    stretch = Exercise(name="Stretching", category="flexibility", equipment_needed=False)

    db.session.add_all([squat, run, stretch])
    db.session.commit()

    print("Creating workout...")

    workout1 = Workout(
        date=date.today(),
        duration_minutes=60,
        notes="Leg day workout"
    )

    db.session.add(workout1)
    db.session.commit()

    print("Linking exercises to workout...")

    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squat.id,
        reps=10,
        sets=4,
        duration_seconds=None
    )

    we2 = WorkoutExercise(
    workout_id=workout1.id,
    exercise_id=run.id,
    reps=1,
    sets=1,
    duration_seconds=600
)

    db.session.add_all([we1, we2])
    db.session.commit()

    print("Seeding complete")