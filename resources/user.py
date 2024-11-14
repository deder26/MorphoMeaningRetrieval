from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models import UserModel
from schemas.userSchema import UserSchema

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, id):
        try:
            user = UserModel.query.get_or_404(id)
            return user
        except Exception as e:
            abort(502, message="Error" + str(e))

    @jwt_required()
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
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users


@blp.route("/user/update")
class UpdateUser(MethodView):
    @jwt_required()
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
