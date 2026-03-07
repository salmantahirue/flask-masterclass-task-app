"""
Flask Application Factory.
Creates and configures the Flask app (Factory Pattern).
"""
from flask import Flask
from config import config_by_name
from app.extensions import db, migrate


def create_app(config_name="development"):
    """
    Application factory: creates a Flask app with the given config.
    Why? So we can have different configs for dev, test, production.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    if config_name == "production" and not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise ValueError("DATABASE_URL must be set in production")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.routes.learn import learn_bp
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.categories import categories_bp
    from app.routes.web import web_bp

    # Learning platform at root (/, /learn/...) — register first so "/" is intro
    app.register_blueprint(learn_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    # Live Task App Demo at /app (login, dashboard, tasks, categories)
    app.register_blueprint(web_bp, url_prefix="/app")

    # Make current_user available in all templates (for nav)
    @app.context_processor
    def inject_current_user():
        from flask import session
        from app.models import User
        uid = session.get("user_id")
        return dict(current_user=db.session.get(User, uid) if uid else None)

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app
