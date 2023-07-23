import functools
from flask_jwt_extended import get_jwt_identity
from init import db
from models.garden import Garden
from models.user import User
from models.comment import Comment
from models.garden_plant import GardenPlant
from models.plant import Plant


# check current user is admin or not
def is_current_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return {"error": "User not found"}, 404
    return user.is_admin


# admin authorisation decorator
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403

    return wrapper


# admin and garden owner authorisation decorator, only admin or owner can update garden info
def authorise_as_admin_or_garden_owner(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Get user id from jwt token (current login user)
        user_id = get_jwt_identity()

        # Database query to get the garden
        stmt = db.select(Garden).filter_by(id=kwargs["garden_id"])
        garden = db.session.scalar(stmt)
        if garden:
            # Check if the user is an admin or the owner of the garden
            if str(garden.user_id) == user_id or is_current_user_admin():
                return fn(*args, **kwargs)
            else:
                return {"error": "Not authorized to perform action"}, 403
        else:
            return {"error": f"Garden id: '{kwargs['garden_id']}' not found"}, 404

    return wrapper


# admin and owner authorisation decorator, only admin or owner can update user info
def authorise_as_account_owner_or_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get user id from jwt token (current login user)
        user_id = get_jwt_identity()

        # Database query to get the user parameter
        # if parameter user id not found in database, return error message
        stmt = db.select(User).filter_by(id=kwargs["user_id"])
        user = db.session.scalar(stmt)

        if not user:
            return {"error": f"User id: '{kwargs['user_id']}' not found"}, 404

        # check if login user is admin or user id in database is the same as the user id passed in parameter
        # if yes, return the function, otherwise return error message
        stmt = db.select(User).filter_by(id=user_id)
        login_user = db.session.scalar(stmt)

        if login_user.is_admin or login_user.id == kwargs["user_id"]:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403

    return wrapper


# query functions, check if the id passed in parameter exists in database
def get_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    return db.session.scalar(stmt)


def get_comment(comment_id, garden_id):
    stmt = db.select(Comment).filter_by(id=comment_id, garden_id=garden_id)
    return db.session.scalar(stmt)


def get_garden(garden_id):
    stmt = db.select(Garden).filter_by(id=garden_id)
    return db.session.scalar(stmt)


def get_plant(plant_id):
    stmt = db.select(Plant).filter_by(id=plant_id)
    return db.session.scalar(stmt)


def get_garden_plant(garden_plant_id, garden_id):
    stmt = db.select(GardenPlant).filter_by(
        garden_id=garden_id, id=garden_plant_id)
    return db.session.scalar(stmt)


def is_admin_or_comment_owner(comment, user_id):
    return str(comment.user_id) == user_id or is_current_user_admin()
