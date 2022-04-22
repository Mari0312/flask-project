from flask import Flask
from database.database import engine, Base
from config import Config


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_table():
            Base.metadata.create_all(bind=engine)


def create_app(config_object=Config):
    app = Flask(__name__)

    app.config.from_object(config_object)

    setup_database(app)

    from .views.user import users_bp
    app.register_blueprint(users_bp)

    return app
