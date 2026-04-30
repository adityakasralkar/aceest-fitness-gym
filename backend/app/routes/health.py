import os

from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return (
        jsonify(
            {
                "status": "ok",
                "service": "aceest-fitness-gym",
                "environment": current_app.config.get("ENVIRONMENT", "unknown"),
                "version": os.getenv("APP_VERSION", "dev"),
                "deployment_variant": os.getenv("DEPLOYMENT_VARIANT", "local"),
            }
        ),
        200,
    )
