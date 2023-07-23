from init import ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And


class GardenSchema (ma.Schema):
    user = fields.Nested("UserSchema", only=["user_name", "email"])
    garden_plants = fields.List(fields.Nested(
        "GardenPlantSchema", exclude=["garden"]))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["garden"]))

    class Meta:
        ordered = True
        fields = ("id", "garden_name", "creation_date",
                  "description", "user", "garden_plants", "comments")

    # fields validation
    garden_name = fields.String(validate=And(Length(
        min=4, error="Garden name must be at least 4 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')))

    description = fields.String(validate=And(Length(
        min=4, error="Description must be at least 4 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')))

    creation_date = fields.Date()


garden_schema = GardenSchema()
gardens_schema = GardenSchema(many=True)
garden_update_schema = GardenSchema(exclude=["garden_plants", "comments"])
