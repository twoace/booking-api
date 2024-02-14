from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bookingapp.schemas import UserSchema, UserUpdateSchema
from bookingapp.models import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from bookingapp.db import db


bp = Blueprint("users", __name__, url_prefix="/user", description="User related operations")


@bp.route("/")
class UserList(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, new_user):
        user = UserModel(**new_user)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred inserting the user")
        return user


@bp.route("/<user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        if user:
            user.name = user_data["name"]
        else:
            user = UserModel(id=user_id, **user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred updating the user")
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred deleting the user")
        return {"message": "User has been deleted successfully"}
