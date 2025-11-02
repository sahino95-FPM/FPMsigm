from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors
from .blueprints import register_blueprints


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    register_blueprints(app)
    return app
