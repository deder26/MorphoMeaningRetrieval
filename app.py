import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from database import db
from jwt_callbacks import configure_jwt_callbacks
from resources.auth import blp as AuthBluePrint
from resources.morpho_analysis import blp as MorphoLogicalAnalysis
from resources.user import blp as UserBluePrint

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = os.getenv("API_TITLE") or "MY_API"
    app.config["API_VERSION"] = os.getenv("API_VERSION") or "v1"
    app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION") or "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "awsedrftgyhujikolp;olljbb")
    api = Api(app)
    jwt = JWTManager(app)
    configure_jwt_callbacks(jwt)
    api.register_blueprint(AuthBluePrint)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(MorphoLogicalAnalysis)
    return app


create_app()
