from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.CheckConstraint("length(name) >= 2", name="check_name_length"),
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        return value

    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ['strength', 'cardio', 'flexibility']
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}")
        return value.lower()

    workout_exercises = db.relationship(
        'WorkoutExercise',
        backref='exercise',
        cascade='all, delete-orphan'
    )


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="check_duration_positive"),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value

    workout_exercises = db.relationship(
        'WorkoutExercise',
        backref='workout',
        cascade='all, delete-orphan'
    )


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint('reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets > 0', name='check_sets_positive'),
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise')
    )

    @validates('reps', 'sets')
    def validate_positive_values(self, key, value):
        if value <= 0:
            raise ValueError(f"{key} must be greater than 0")
        return value