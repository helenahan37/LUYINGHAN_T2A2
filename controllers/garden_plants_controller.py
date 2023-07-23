from flask import Blueprint, request
from init import db
from models.garden import Garden
from flask_jwt_extended import jwt_required
from schemas.garden_plant_schema import garden_plant_schema, garden_plants_schema
from models.garden_plant import GardenPlant
from models.plant import Plant
from auth_deco import authorise_as_admin_or_garden_owner, get_garden_plant, get_garden
from schemas.garden_plant_schema import validate_position
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


garden_plant_bp = Blueprint("garden_plant", __name__)


# garden/garden_id/plant/plant_id -post route
# login user can add plant to their own garden, admin can add plant to any garden
@garden_plant_bp.route("/plant/<int:plant_id>", methods=["POST"])
@jwt_required()
@authorise_as_admin_or_garden_owner
def create_garden_plants(garden_id, plant_id):
    try:
        body_data = garden_plant_schema.load(request.get_json())

        # check if the position is been taken in this garden
        validate_position(garden_id, body_data.get("position"))

        garden = db.session.query(Garden).get(garden_id)
        plant = db.session.query(Plant).get(plant_id)

        # if garden and plant exists, create new garden_plant
        if garden and plant:
            garden_plant = GardenPlant(
                color=body_data.get("color"),
                position=body_data.get("position"),
                size=body_data.get("size"),
                garden_id=garden_id,
                plant_id=plant_id,
            )
            db.session.add(garden_plant)
            db.session.commit()
            return garden_plant_schema.dump(garden_plant), 201
        else:
            return {"error": f"Plant id {plant_id} not found"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            column_name = err.orig.diag.column_name
            return {"error": f"{column_name} is required."}, 401


# garden/garden_id/garden_plant -get route
# get all garden_plants from a garden
# all visitors can get garden_plants from any garden
@garden_plant_bp.route("/garden_plants", methods=["GET"])
def get_garden_plants(garden_id):
    garden = get_garden(garden_id)
    if not garden:
        return {"error": f"Garden id:'{garden_id}' not found"}, 404

    garden_plants = GardenPlant.query.filter_by(
        garden_id=garden_id).order_by(GardenPlant.id).all()
    if garden_plants:
        return garden_plants_schema.dump(garden_plants), 200
    else:
        return {"error": f"No garden_plants found in garden id: '{garden_id}'"}, 404


# garden/garden_id/garden_plant/garden_plant_id -update route
# only user can update their own garden_plant, admin can update any garden_plant
@garden_plant_bp.route("/garden_plant/<int:garden_plant_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin_or_garden_owner
def update_garden_plant(garden_id, garden_plant_id):

    body_data = garden_plant_schema.load(request.get_json())

    # select garden_plant by id from garden id
    garden_plant = get_garden_plant(garden_plant_id, garden_id)
    if not garden_plant:
        return {"error": f"GardenPlant id '{garden_plant_id}' not found in garden id '{garden_id}'"}, 404

    '''
    check if the request position has been changed compared to the current position
    if not changed, no need to validate, update garden_plant attributes
    '''
    requested_position = body_data.get("position")
    if requested_position != garden_plant.position:
        validate_position(garden_id, requested_position)

    # Update garden_plant attributes
    garden_plant.color = body_data.get("color", garden_plant.color)
    garden_plant.position = body_data.get("position", garden_plant.position)
    garden_plant.size = body_data.get("size", garden_plant.size)
    db.session.commit()
    return garden_plant_schema.dump(garden_plant), 200


# garden/garden_id/garden_plant/garden_plant_id -delete route
# login user can delete plant from their own garden, admin can delete plant from any garden
@garden_plant_bp.route("/garden_plant/<int:garden_plant_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin_or_garden_owner
def delete_garden_plants(garden_id, garden_plant_id):

    # select garden_plant by id from garden id
    garden_plant = get_garden_plant(garden_plant_id, garden_id)
    if garden_plant:
        db.session.delete(garden_plant)
        db.session.commit()
        return {"message": f"GardenPlant id: '{garden_plant_id}' successfully deleted from garden id: '{garden_id}'"}, 200
    else:
        return {"error": f"GardenPlant id: '{garden_plant_id}' not found in garden id: '{garden_id}'"}, 404
