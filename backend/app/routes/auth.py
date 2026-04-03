from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db, bcrypt, limiter
from app.models.database import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["username", "password"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if len(data["username"]) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400

    existing = User.query.filter_by(username=data["username"]).first()
    if existing:
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        username=data["username"],
        password=hashed_password,
        role=data.get("role", "Trainer")
    )

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity=user.username,
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.username,
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    
    access_token = create_access_token(
        identity=identity,
        additional_claims={"role": user.role}
    )
    
    return jsonify({
        "access_token": access_token
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"}), 200