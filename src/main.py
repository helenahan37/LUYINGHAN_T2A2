from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.garden_controller import garden_bp
from controllers.plant_controller import plant_bp
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError


def create_app():
    # Creating the flask app object
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Error handlers
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        return {'error': str(err)}, 400

    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        return {"error": "Invalid or missing JWT"}, 401

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    # create database, marshmallow, bcrypt, jwt objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registering blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(garden_bp)
    app.register_blueprint(plant_bp)

    # Welcome route

    @app.get('/')
    def hello():
        return {"message": "Welcome to the Virtual Garden API! Create your dream garden with ease🔮"}
    return app
