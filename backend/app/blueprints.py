from .controllers.credef_controller import bp as credef_bp


def register_blueprints(app):
    app.register_blueprint(credef_bp)
