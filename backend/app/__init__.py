from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.routes.clients import clients_bp
    from app.routes.programs import programs_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(clients_bp, url_prefix="/api/clients")
    app.register_blueprint(programs_bp, url_prefix="/api/programs")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        db.create_all()

    return app