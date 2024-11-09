import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from database import db


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "MorphoAnalysis"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.config["JWT_SECRET_KEY"] = (
        "npMHarFza7R8FM1Xc02EF6SNXeoqBsf70NKM3hmten3a1Oy7kDEvT7nNRs/tg0Og"
    )
    api = Api(app)
    jwt = JWTManager(app)
    api.register_blueprint(AuthorBluePrint)
    api.register_blueprint(BookBluePrint)
    api.register_blueprint(UserBluePrint)

    return app


create_app(db_url=None)
