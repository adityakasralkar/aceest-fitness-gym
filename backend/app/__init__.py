from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config
import os

db = SQLAlchemy()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.routes.clients import clients_bp
    from app.routes.programs import programs_bp

    app.register_blueprint(clients_bp, url_prefix="/api/clients")
    app.register_blueprint(programs_bp, url_prefix="/api/programs")

    with app.app_context():
        db.create_all()

    return app
