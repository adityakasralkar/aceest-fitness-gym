from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.database import Progress, Client
from datetime import datetime

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/<string:client_name>", methods=["GET"])
@jwt_required()
def get_progress(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    progress = Progress.query.filter_by(client_name=client_name).all()
    return jsonify([p.to_dict() for p in progress]), 200


@progress_bp.route("/<string:client_name>", methods=["POST"])
@jwt_required()
def add_progress(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "adherence" not in data:
        return jsonify({"error": "adherence is required"}), 400

    if not isinstance(data["adherence"], int) or not 0 <= data["adherence"] <= 100:
        return jsonify({"error": "adherence must be between 0 and 100"}), 400

    progress = Progress(
        client_name=client_name,
        week=data.get("week", datetime.now().strftime("Week %U - %Y")),
        adherence=data["adherence"]
    )

    db.session.add(progress)
    db.session.commit()
    return jsonify(progress.to_dict()), 201


@progress_bp.route("/<string:client_name>/<int:progress_id>", methods=["DELETE"])
@jwt_required()
def delete_progress(client_name, progress_id):
    progress = Progress.query.filter_by(
        id=progress_id, client_name=client_name
    ).first()

    if not progress:
        return jsonify({"error": "Progress record not found"}), 404

    db.session.delete(progress)
    db.session.commit()
    return jsonify({"message": "Progress record deleted"}), 200