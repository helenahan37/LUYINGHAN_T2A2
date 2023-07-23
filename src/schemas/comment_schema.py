from init import ma
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp


class CommentSchema(ma.Schema):
    # tell marshmallow which schema to use to convert model format to python object
    # one comment can only have one user and one garden
    user = fields.Nested("UserSchema", only=[
        "user_name", "email"])
    garden = fields.Nested("GardenSchema", exclude=[
        "comments", "garden_plants"])

    class Meta:
        ordered = True
        fields = ("id", "comment_date", "message", "garden", "user")

    # validate message , message must be at least 4 characters long and only letters, spaces and numbers are allowed
    message = fields.String(validate=And(Length(
        min=4, error="Message must be at least 4 characters long"),
        Regexp('^[a-zA-Z]',
               error='Must begin with a letter')), required=True)

    comment_date = fields.Date()


comment_schema = CommentSchema()
comments_schema = CommentSchema(exclude=["garden"], many=True)
update_comment_schema = CommentSchema(exclude=["garden"])
