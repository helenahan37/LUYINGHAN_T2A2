from flask import Blueprint, request
from init import db, bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
from models.user import User
from schemas.user_schema import user_schema, users_schema, get_user_schema, update_user_schema, user_register_schema
from flask_jwt_extended import jwt_required
from auth_deco import authorise_as_admin, authorise_as_account_owner_or_admin, is_current_user_admin, get_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# auth/register -user register route
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # get body request
        body_data = user_schema.load(request.get_json())

        # Create a new User model instance from the user info
        # instance of user class which is in turn a sqlalchemy model
        user = User()
        # create new user from request
        user.user_name = body_data.get("user_name")
        user.email = body_data.get("email")
        if body_data.get("password"):
            user.password = bcrypt.generate_password_hash(
                body_data.get("password")).decode("utf-8")
        # add new user to session
        db.session.add(user)
        # commit to add the user to database
        db.session.commit()
        # response to the client
        return user_register_schema.dump(user), 201
    except IntegrityError as err:
        db.session.rollback()
        # check if user_name provided
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            column_name = err.orig.diag.column_name
            return {"error": f"{column_name} is required."}, 401
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint_name = err.orig.diag.constraint_name
            # check if email is registered
            if constraint_name == "users_email_key":
                return {"error": f"Email '{user.email}' is registered."}, 409
            # check if username is registered
            elif constraint_name == "users_user_name_key":
                return {"error": f"user name '{user.user_name}' is registered."}, 409
    return {"error": f"An error occurred while registering the user."}, 500


# auth/user - get all users routes
# only admin can get all users
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
@authorise_as_admin
def auth_user():
    stmt = db.select(User).order_by(User.id)
    users_list = db.session.scalars(stmt)
    result = users_schema.dump(users_list)
    return result


# auth/user/user_id - get user by id route
# only admin can get user by id
@auth_bp.route("/user/<int:id>", methods=["GET"])
@jwt_required()
@authorise_as_admin
def auth_user_by_id(id):
    user = get_user(id)
    if not user:
        return {"error": f"User id:'{id}' not found"}, 404
    result = get_user_schema.dump(user)
    return result


# auth/login - user login route
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    body_data = user_schema.load(request.get_json())
    if not body_data.get("email") or not body_data.get("password"):
        return {"error": "Please provide your email and password"}, 401

    # Find the user by email address
    stmt = db.select(User).filter(
        User.email == body_data.get("email"))  # get user from database
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(
            user.id), expires_delta=timedelta(days=1))
        return {"user_name": user.user_name, "email": user.email, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401


# auth/user/user_id - update user account route, only admin can change is_admin status
# only admin and account owner can update user account info
@auth_bp.route("/user/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_account_owner_or_admin
def auth_update_user(user_id):
    try:
        body_data = user_schema.load(request.get_json())

        # get user from database
        update_user = get_user(user_id)

        # update user info from request
        update_user.user_name = body_data.get(
            "user_name") or update_user.user_name
        update_user.email = body_data.get("email") or update_user.email

        if body_data.get("password"):
            update_user.password = bcrypt.generate_password_hash(
                body_data["password"]).decode("utf-8")
        else:
            update_user.password = update_user.password

        # only current admin user can change the is_admin status
        if "is_admin" in body_data and body_data["is_admin"] != update_user.is_admin:
            if not is_current_user_admin():
                return {"error": "Not authorized to modify 'admin' status"}, 403
            '''
            make sure updated boolean value is passed correctly to the database instead of using 'or' operator
            '''
            update_user.is_admin = body_data.get(
                "is_admin", update_user.is_admin)
        db.session.add(update_user)
        db.session.commit()
        return update_user_schema.dump(update_user)
    except IntegrityError as err:
        db.session.rollback()
        # check if update user info - user email and username already exists
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint_name = err.orig.diag.constraint_name
            # check if email is already in use
            if constraint_name == "users_email_key":
                return {"error": f"Email '{body_data.get('email')}' is registered."}, 409
            # check if username is already in use
            elif constraint_name == "users_user_name_key":
                return {"error": f"Username '{body_data.get('user_name')}' already exists."}, 409
    return {"error": f"An error occurred while updating the user."}, 500


# auth/user/user_id - delete user account route
# only admin and owner can delete user account
@auth_bp.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_account_owner_or_admin
def user_delete(user_id):
    user = get_user(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User: '{user.email}' successfully deleted."}, 200
