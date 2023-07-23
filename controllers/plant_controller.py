from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.plant import Plant
from schemas.plant_schema import plant_schema, plant_update_schema, plants_update_schema
from flask_jwt_extended import jwt_required
from auth_deco import authorise_as_admin, get_plant


plant_bp = Blueprint("plant", __name__, url_prefix="/plant")


# plants -get route
# all visitors can access this route
@plant_bp.route("/", methods=["GET"])
def get_all_plants():
    stmt = db.select(Plant).order_by(Plant.id)
    plants = db.session.scalars(stmt)
    return plants_update_schema.dump(plants), 200


# get a plant by id -get route
# all visitors can access this route
@plant_bp.route("/<int:id>", methods=["GET"])
def get_plant_by_id(id):
    plant = get_plant(id)
    if plant:
        return plant_schema.dump(plant), 200
    else:
        return {"message": f"Plant id:'{id}' not found"}, 404


# post new plant route
# only admin can post a new plant
@plant_bp.route("/", methods=["POST"])
@jwt_required()
@authorise_as_admin
def create_plant():
    try:
        body_data = plant_schema.load(request.get_json())
        plant = Plant(
            plant_name=body_data.get("plant_name"),
            genus=body_data.get("genus"),
            watering=body_data.get("watering"),
            growth_rate=body_data.get("growth_rate")
        )
        db.session.add(plant)
        db.session.commit()
        return plant_update_schema.dump(plant), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"Plant name: '{body_data.get('plant_name')}' already exists"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required'}, 400


# update plant route
# only admin can update a plant
@plant_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@ authorise_as_admin
def update_plant(id):
    try:
        body_data = plant_schema.load(request.get_json())
        plant = get_plant(id)
        if plant:
            plant.plant_name = body_data.get("plant_name") or plant.plant_name
            plant.genus = body_data.get("genus") or plant.genus
            plant.watering = body_data.get("watering") or plant.watering
            plant.growth_rate = body_data.get(
                "growth_rate") or plant.growth_rate
            db.session.commit()
            return plant_update_schema.dump(plant), 200
        else:
            return {"message": f"Plant id:'{id}' not found"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"Garden name: '{body_data.get('plant_name')}' already exists"}, 409


# plant delete route
# only admin can delete a plant

@plant_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@ authorise_as_admin
def delete_plant(id):
    plant = get_plant(id)
    if plant:
        db.session.delete(plant)
        db.session.commit()
        return {"message": f"Plant name: '{plant.plant_name}' deleted successfully"}, 200
    else:
        return {"message": f"Plant id:'{id}' not found"}, 404
