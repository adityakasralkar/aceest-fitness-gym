from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.database import Workout, Client
from datetime import date

workouts_bp = Blueprint("workouts", __name__)


@workouts_bp.route("/<string:client_name>", methods=["GET"])
@jwt_required()
def get_workouts(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    workouts = Workout.query.filter_by(client_name=client_name).all()
    return jsonify([w.to_dict() for w in workouts]), 200


@workouts_bp.route("/<string:client_name>", methods=["POST"])
@jwt_required()
def add_workout(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["workout_type", "duration_min"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    valid_types = ["Strength", "Hypertrophy", "Cardio", "Mobility", "HIIT"]
    if data["workout_type"] not in valid_types:
        return jsonify({"error": f"workout_type must be one of {valid_types}"}), 400

    if not isinstance(data["duration_min"], int) or data["duration_min"] <= 0:
        return jsonify({"error": "duration_min must be a positive integer"}), 400

    workout = Workout(
        client_name=client_name,
        date=data.get("date", date.today().isoformat()),
        workout_type=data["workout_type"],
        duration_min=data["duration_min"],
        notes=data.get("notes", "")
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout.to_dict()), 201


@workouts_bp.route("/<string:client_name>/<int:workout_id>", methods=["PUT"])
@jwt_required()
def update_workout(client_name, workout_id):
    workout = Workout.query.filter_by(
        id=workout_id,
        client_name=client_name
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()

    if "workout_type" in data:
        workout.workout_type = data["workout_type"]
    if "duration_min" in data:
        workout.duration_min = data["duration_min"]
    if "notes" in data:
        workout.notes = data["notes"]
    if "date" in data:
        workout.date = data["date"]

    db.session.commit()
    return jsonify(workout.to_dict()), 200


@workouts_bp.route("/<string:client_name>/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(client_name, workout_id):
    workout = Workout.query.filter_by(
        id=workout_id,
        client_name=client_name
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200