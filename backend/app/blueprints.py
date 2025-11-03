from .controllers.credef_controller import bp as credef_bp
from .controllers.auth_controller import bp as auth_bp


def register_blueprints(app):
    app.register_blueprint(credef_bp)
    app.register_blueprint(auth_bp)
