from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    jwt = JWTManager(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app