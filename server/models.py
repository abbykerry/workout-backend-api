from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # 🔒 Table Constraints (EXCELLENT LEVEL)
    __table_args__ = (
        db.CheckConstraint("length(name) >= 2", name="check_name_length"),
    )

    # 🧠 Model Validations (EXCELLENT LEVEL)
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