from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app= Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.reflex import Reflex
    from app.models.diary import Diary


    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.diary_routes import diary_bp
    app.register_blueprint(diary_bp)

    from .routes.reflex_routes import reflex_bp
    app.register_blueprint(reflex_bp)
    
    CORS(app)
    return app