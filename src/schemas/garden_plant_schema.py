from init import ma, db
from marshmallow import fields, validates
from models.garden_plant import GardenPlant
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError


VALID_COLORS = ["Green", "Red", "Yellow",
                "Orange", "Purple", "Blue", "Rainbow"]
VALID_POSITIONS = ["Center", "South", "North", "East",
                   "West", "Northeast", "Northwest", "Southeast", "Southwest"]
VALID_SIZES = ["Small", "Medium", "Large"]


class GardenPlantSchema(ma.Schema):

    # one garden_plant can only have one garden and one plant
    garden = fields.Nested("GardenSchema", only=[
        "id", "garden_name", "user"])
    plant = fields.Nested("PlantSchema", only=["id", "plant_name"])

    class Meta:
        ordered = True
        fields = ("id", "plant", "color", "position",
                  "size", "garden")

    # fields validation
    color = fields.String(validate=OneOf(VALID_COLORS))
    position = fields.String(validate=OneOf(
        VALID_POSITIONS))
    size = fields.String(validate=OneOf(VALID_SIZES))


@validates("position")
def validate_position(garden_id, body_position):
    # Check if position is already occupied in this garden
    # compare database with the parameter
    count = GardenPlant.query.filter_by(
        garden_id=garden_id, position=body_position).count()
    if count > 0:
        raise ValidationError(
            f"Position '{body_position}' already been occupied")

    return body_position


garden_plant_schema = GardenPlantSchema()
garden_plants_schema = GardenPlantSchema(exclude=["garden"], many=True)
