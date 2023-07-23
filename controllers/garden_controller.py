from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.garden import Garden
from datetime import date
from schemas.garden_schema import garden_schema, gardens_schema, garden_update_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.garden_plants_controller import garden_plant_bp
from controllers.comment_controller import comment_bp
from auth_deco import get_garden, authorise_as_admin_or_garden_owner

garden_bp = Blueprint("garden", __name__, url_prefix="/garden")
garden_bp.register_blueprint(
    garden_plant_bp, url_prefix="/<int:garden_id>")
garden_bp.register_blueprint(comment_bp, url_prefix="/<int:garden_id>/comment")


# garden/-get all gardens route
# all visitors can access this route
@garden_bp.route("/", methods=["GET"])
def get_all_gardens():
    stmt = db.select(Garden).order_by(Garden.id.desc())
    gardens = db.session.scalars(stmt)
    return gardens_schema.dump(gardens), 200


# garden/garden_id-get garden by id route
# all users can get the garden by id
@garden_bp.route("/<int:id>", methods=["GET"])
def get_garden_by_id(id):
    garden = get_garden(id)
    if garden:
        return garden_schema.dump(garden), 200
    else:
        return {"error": f"Garden id:'{id}' not found"}, 404


# garden/ -post garden route
# only register user can post a new garden
@garden_bp.route("/", methods=["POST"])
@jwt_required()
def create_garden():
    try:
        body_data = garden_schema.load(request.get_json())
        # create new garden instance
        garden = Garden(
            garden_name=body_data.get("garden_name"),
            description=body_data.get("description"),
            creation_date=date.today(),
            user_id=get_jwt_identity()
        )
        db.session.add(garden)
        db.session.commit()
        return garden_update_schema.dump(garden), 201
    except IntegrityError as err:
        # check garden_name provided or not
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": "'garden_name' is required"}, 400
        elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # check if garden_name already exists
            return {"error": f"Garden name: '{body_data.get('garden_name')}' already exists"}, 409

    return {"error": "An error occurred while creating the garden"}, 500


# garden/garden_id -update route
# only admin and garden owner can update garden info
@garden_bp.route("/<int:garden_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin_or_garden_owner
def update_garden(garden_id):
    try:
        body_data = garden_schema.load(request.get_json())

        # get garden by id from database
        garden = get_garden(garden_id)
        if garden:
            garden.garden_name = body_data.get(
                "garden_name") or garden.garden_name
            garden.description = body_data.get(
                "description") or garden.description
            db.session.commit()
            return garden_update_schema.dump(garden), 200
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"Garden name: '{body_data.get('garden_name')}' already exists"}, 409


# garden/garden_id -delete route
# only admin and garden owner can delete garden
@garden_bp.route("/<int:garden_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin_or_garden_owner
def delete_garden(garden_id):
    garden = get_garden(garden_id)

    if not garden:
        return {"error": f"Garden id:'{garden_id}' not found"}, 404

    db.session.delete(garden)
    db.session.commit()
    return {"message": f"Garden name:'{garden.garden_name}' successfully deleted"}, 200
