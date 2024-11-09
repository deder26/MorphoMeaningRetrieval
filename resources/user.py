from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import UserModel
from schemas.userSchema import UserSchema

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
        try:
            user = UserModel.query.get_or_404(id)
            return user
        except Exception as e:
            abort(502, message="Error" + str(e))

    def delete(self, id):
        try:
            user = UserModel.query.get_or_404(id)
            db.session().delete(user)
            db.session().commit()
            return {"message": "successfully deleted"}, 200
        except (SQLAlchemyError, Exception) as e:
            db.session().rollback()
            abort(500, message="Error" + str(e))


@blp.route("/users")
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users


@blp.route("/user/create")
class CreateUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, requested_data):
        try:
            user = UserModel(**requested_data)
            user.password = pbkdf2_sha256.hash(user.password)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as IE:
            abort(400, message="Error: " + str(IE))
        except SQLAlchemyError as SQE:
            abort(500, message="Error: " + str(SQE))
        except Exception as ex:
            abort(500, message="Error: " + str(ex))


@blp.route("/user/update")
class UpdateUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, request_data):
        try:
            user = UserModel.query.get_or_404(request_data["id"])
            if user:
                user.name = request_data["name"]
                user.email = request_data["email"]
                db.session.add(user)
                db.session.commit()
                return user
        except SQLAlchemyError as sc:
            abort(502, message="Server Error1", error=str(sc))
        except Exception as e:
            abort(502, message="Server Error2" + str(e), error=str(e))
