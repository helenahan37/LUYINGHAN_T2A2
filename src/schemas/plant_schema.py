from init import ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And, OneOf

VALID_WATERING = ["Frequent", "Average", "Minimal"]
VALID_GROWTH_RATE = ["High", "Moderate", "Low"]


class PlantSchema (ma.Schema):

    # one to many relationship, one plant can have many garden_plants
    garden_plants = fields.List(fields.Nested(
        "GardenPlantSchema", exclude=["plant"]))

    class Meta:
        ordered = True
        fields = ("id", "plant_name", "genus",
                  "watering", "growth_rate", "garden_plants")

    # fields validation
    plant_name = fields.String(validate=And(Length(
        min=4, error="Garden name must be at least 4 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')))

    genus = fields.String(validate=And(Length(
        min=4, error="Genus must be at least 4 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')))

    watering = fields.String(validate=OneOf(VALID_WATERING))
    growth_rate = fields.String(validate=OneOf(VALID_GROWTH_RATE))


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
plant_update_schema = PlantSchema(exclude=["garden_plants"])
plants_update_schema = PlantSchema(exclude=["garden_plants"], many=True)
