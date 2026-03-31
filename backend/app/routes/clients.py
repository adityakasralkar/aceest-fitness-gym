from flask import Blueprint, request, jsonify
from app import db
from app.models.database import Client
from app.services.calculator import calculate_calories

clients_bp = Blueprint("clients", __name__)

# GET all clients
@clients_bp.route("/", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients]), 200

# GET single client
@clients_bp.route("/<string:name>", methods=["GET"])
def get_client(name):
    client = Client.query.filter_by(name=name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client.to_dict()), 200

# POST create client
@clients_bp.route("/", methods=["POST"])
def create_client():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["name", "age", "weight", "program"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    existing = Client.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Client already exists"}), 409

    try:
        calories = calculate_calories(data["weight"], data["program"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    client = Client(
        name=data["name"],
        age=data["age"],
        weight=data["weight"],
        program=data["program"],
        calories=calories
    )

    db.session.add(client)
    db.session.commit()

    return jsonify(client.to_dict()), 201

# PUT update client
@clients_bp.route("/<string:name>", methods=["PUT"])
def update_client(name):
    client = Client.query.filter_by(name=name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()

    if "weight" in data:
        client.weight = data["weight"]
    if "age" in data:
        client.age = data["age"]
    if "program" in data:
        client.program = data["program"]
        client.calories = calculate_calories(client.weight, data["program"])

    db.session.commit()
    return jsonify(client.to_dict()), 200

# DELETE client
@clients_bp.route("/<string:name>", methods=["DELETE"])
def delete_client(name):
    client = Client.query.filter_by(name=name).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": f"Client {name} deleted"}), 200
