from flask import Blueprint, jsonify, request
from app.services.calculator import get_all_programs, get_program, calculate_calories

programs_bp = Blueprint("programs", __name__)


# GET all programs
@programs_bp.route("/", methods=["GET"])
def get_programs():
    programs = get_all_programs()
    return jsonify(programs), 200


# GET single program
@programs_bp.route("/<string:name>", methods=["GET"])
def get_single_program(name):
    try:
        program = get_program(name)
        return jsonify(program), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# POST calculate calories
@programs_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "weight" not in data or "program" not in data:
        return jsonify({"error": "weight and program are required"}), 400

    try:
        calories = calculate_calories(data["weight"], data["program"])
        return (
            jsonify({"weight": data["weight"], "program": data["program"], "calories": calories}),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
