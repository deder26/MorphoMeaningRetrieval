from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib import pbkdf2_sha256
from sqlalchemy.exc import IdentifierError, IntegrityError, SQLAlchemyError

from database import db
from models import UserModel
from schemas.userSchema import UserLoginSchema, UserSchema

blp = Blueprint("user_auth", __name__, descriptios="user auth operations")


@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, request):
        try:
            user = UserModel(**request)
            user.password = pbkdf2_sha256.hash(user.password)
            db.session.add(user)
            db.session.commit()
        except (SQLAlchemyError, IntegrityError, IdentifierError, Exception) as err:
            db.session.rollback()
            abort(500, message="Error Occured" + str(err))


@blp.route("/login")
def get(self):
    @blp.arguments(UserLoginSchema)
    def post(self, request):
        try:
            user = UserModel.query.filter(email=request["email"]).first()
            if user and pbkdf2_sha256.hash(request["password"]) == user.password:
                return {"message": "successfully logged in"}, 200
            else:
                return {"message": "password not matched"}, 419
        except (SQLAlchemyError, IntegrityError, IdentifierError, Exception) as err:
            db.session.rollback()
            abort(500, message="Error Occured" + str(err))


@blp.route("/logout")
def get(self):
    pass
