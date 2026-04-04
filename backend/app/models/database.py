from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="Trainer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float)
    program = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer)
    target_weight = db.Column(db.Float)
    membership_status = db.Column(db.String(20), default="Active")
    membership_end = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workouts = db.relationship("Workout", backref="client", lazy=True)
    progress = db.relationship("Progress", backref="client", lazy=True)
    metrics = db.relationship("Metric", backref="client", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "program": self.program,
            "calories": self.calories,
            "target_weight": self.target_weight,
            "membership_status": self.membership_status,
            "membership_end": self.membership_end,
            "created_at": self.created_at.isoformat(),
        }


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey("clients.name"), nullable=False)
    date = db.Column(db.String(20))
    workout_type = db.Column(db.String(50))
    duration_min = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "date": self.date,
            "workout_type": self.workout_type,
            "duration_min": self.duration_min,
            "notes": self.notes,
        }


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey("clients.name"), nullable=False)
    week = db.Column(db.String(20))
    adherence = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "week": self.week,
            "adherence": self.adherence,
        }


class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey("clients.name"), nullable=False)
    date = db.Column(db.String(20))
    weight = db.Column(db.Float)
    waist = db.Column(db.Float)
    bodyfat = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "date": self.date,
            "weight": self.weight,
            "waist": self.waist,
            "bodyfat": self.bodyfat,
        }
