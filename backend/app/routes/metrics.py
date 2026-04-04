from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.database import Metric, Client
from datetime import date

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/<string:client_name>", methods=["GET"])
@jwt_required()
def get_metrics(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    metrics = Metric.query.filter_by(client_name=client_name).all()
    return jsonify([m.to_dict() for m in metrics]), 200


@metrics_bp.route("/<string:client_name>", methods=["POST"])
@jwt_required()
def add_metric(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if not any(k in data for k in ["weight", "waist", "bodyfat"]):
        return jsonify({"error": "At least one metric required"}), 400

    if "bodyfat" in data and not 0 <= data["bodyfat"] <= 100:
        return jsonify({"error": "bodyfat must be between 0 and 100"}), 400

    metric = Metric(
        client_name=client_name,
        date=data.get("date", date.today().isoformat()),
        weight=data.get("weight"),
        waist=data.get("waist"),
        bodyfat=data.get("bodyfat"),
    )

    db.session.add(metric)
    db.session.commit()
    return jsonify(metric.to_dict()), 201


@metrics_bp.route("/<string:client_name>/<int:metric_id>", methods=["DELETE"])
@jwt_required()
def delete_metric(client_name, metric_id):
    metric = Metric.query.filter_by(id=metric_id, client_name=client_name).first()

    if not metric:
        return jsonify({"error": "Metric not found"}), 404

    db.session.delete(metric)
    db.session.commit()
    return jsonify({"message": "Metric deleted"}), 200
