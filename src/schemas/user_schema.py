from init import ma
from marshmallow import fields
from marshmallow.validate import Length, Email, Regexp, And


class UserSchema(ma.Schema):  # User register schema
    # tell marshmallow which schema to use to convert model format to python object
    # fields.Nested() is used to nest a schema within a schema
    # one to many relationship, one user can have many gardens and comments
    gardens = fields.List(fields.Nested("GardenSchema", exclude=["user"]))
    comments = fields.List(fields.Nested(
        "CommentSchema", only=["comment_date", "message"]))

    class Meta:
        ordered = True
        fields = ("id", "user_name", "email",
                  "password", "is_admin", "gardens", "comments")
    # fields validation
    password = fields.String(
        validate=Length(
            min=6, error="Password must be at least 6 characters long.")
    )

    email = fields.String(validate=Email(
        error="Invalid email format. Please provide a valid email address."))

    user_name = fields.String(validate=And(
        Length(min=4, error='Username must be at least 4 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')
    ))


user_schema = UserSchema()
users_schema = UserSchema(
    exclude=["gardens", "password", "comments"], many=True)
get_user_schema = UserSchema(exclude=["password", "comments"])
update_user_schema = UserSchema(exclude=["gardens", "password", "comments"])
user_register_schema = UserSchema(only=["id", "user_name", "email"])
