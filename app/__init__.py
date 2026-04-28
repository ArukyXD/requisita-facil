from flask import Flask
from dotenv import load_dotenv
import os

from app.extensions import db, login_manager
from app.models import User
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.materials import materials_bp
from app.routes.requisitions import requisitions_bp


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(materials_bp)
    app.register_blueprint(requisitions_bp)

    return app
