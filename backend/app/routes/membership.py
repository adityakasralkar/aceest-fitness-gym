from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.database import Client
from datetime import datetime, timedelta

membership_bp = Blueprint("membership", __name__)


@membership_bp.route("/<string:client_name>", methods=["GET"])
@jwt_required()
def get_membership(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    return jsonify({
        "client_name": client_name,
        "membership_status": client.membership_status,
        "membership_end": client.membership_end
    }), 200


@membership_bp.route("/<string:client_name>/renew", methods=["POST"])
@jwt_required()
def renew_membership(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()
    months = data.get("months", 1)

    if not isinstance(months, int) or months <= 0:
        return jsonify({"error": "months must be a positive integer"}), 400

    end_date = datetime.now() + timedelta(days=30 * months)
    client.membership_status = "Active"
    client.membership_end = end_date.strftime("%Y-%m-%d")

    db.session.commit()

    return jsonify({
        "message": f"Membership renewed for {months} month(s)",
        "client_name": client_name,
        "membership_status": client.membership_status,
        "membership_end": client.membership_end
    }), 200


@membership_bp.route("/<string:client_name>/cancel", methods=["POST"])
@jwt_required()
def cancel_membership(client_name):
    client = Client.query.filter_by(name=client_name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    client.membership_status = "Cancelled"
    db.session.commit()

    return jsonify({
        "message": "Membership cancelled",
        "client_name": client_name,
        "membership_status": client.membership_status
    }), 200