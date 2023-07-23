from flask import Blueprint, request
from init import db
from models.comment import Comment
from datetime import date
from schemas.comment_schema import comment_schema, comments_schema, update_comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth_deco import get_comment, get_garden, is_admin_or_comment_owner


comment_bp = Blueprint("comment", __name__)


#  garden/garden_id/comment -post route
# only login user can post a new comment by garden id
@comment_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(garden_id):

    body_data = comment_schema.load(request.get_json())

    # select garden from database by id
    garden = get_garden(garden_id)

    if garden:
        # create new comment
        comment = Comment(
            message=body_data.get("message"),
            comment_date=date.today(),
            user_id=get_jwt_identity(),
            garden_id=garden_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {"error": f"Garden:'{garden_id} not found"}, 404


# garden/garden_id/comment -get route
# only login user can get all comments by garden id
@comment_bp.route("/", methods=["GET"])
@jwt_required()
def get_comments_by_garden_id(garden_id):

    # check if garden id exists or not
    garden = get_garden(garden_id)
    if not garden:
        return {"error": f"Garden id:'{garden_id}' not found"}, 404

    # get all comments by garden id
    comment = Comment.query.filter_by(
        garden_id=garden_id).order_by(Comment.comment_date.desc()).all()

    # if comments found return comments, else return message
    if comment:
        return comments_schema.dump(comment), 200
    else:
        return {"message": f"No comment found for garden id '{garden_id}'"}, 200


# garden/garden_id/comment/comment_id -put route
# only login comment owner and admin can update comment by comment id
@comment_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_comment(garden_id, comment_id):
    user_id = get_jwt_identity()

    # check if garden id exists or not
    garden = get_garden(garden_id)
    if not garden:
        return {"error": f"Garden id:'{garden_id}' not found"}, 404

    # get selected comment from database by garden and comment id
    comment = get_comment(comment_id, garden_id)
    body_data = update_comment_schema.load(request.get_json())

    # if comment id found check the user is admin or comment owner
    # if admin or comment owner update the comment, else return error
    if comment:
        if is_admin_or_comment_owner(comment, user_id):
            comment.message = body_data.get("message") or comment.message
            db.session.commit()
            return update_comment_schema.dump(comment), 200
        else:
            return {"error": "Not authorized to perform action"}, 403
    else:
        return {"error": f"Comment id: '{comment_id}' not found for garden id: '{garden_id}'"}, 404


# garden/garden_id/comment/comment_id -delete route
# only admin and comment owner can delete comment by comment id
@comment_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(garden_id, comment_id):
    # Get user id from jwt token (current login user)
    user_id = get_jwt_identity()

    # get selected comment from database by garden and comment id
    comment = get_comment(comment_id, garden_id)
    garden = get_garden(garden_id)

    # if garden id not found return error
    if not garden:
        return {"error": f"Garden id:'{garden_id}' not found"}, 404

    # if comment id found check the user is admin or comment owner
    # if admin or comment owner delete the comment, else return error
    if comment:
        if is_admin_or_comment_owner(comment, user_id):
            db.session.delete(comment)
            db.session.commit()
            return {"message": f"Comment message:'{comment.message}' was deleted successfully"}, 200
        else:
            return {"error": "Not authorized to perform action"}, 403
    else:
        return {"error": f"Comment id: '{comment_id}' not found for garden id: '{garden_id}'"}, 404
