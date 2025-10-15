from app.extensions import ma
from app.models.user import User
from marshmallow import Schema, fields


class UserCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True, load_only=True)

    tasks = ma.Nested('TaskSchema', many=True)
    tags = ma.Nested('TagSchema', many=True)


# Schema de entrada para login
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# Schema de entrada para signup
class UserSignupSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


user_complete_schema = UserCompleteSchema()
user_login_schema = UserLoginSchema()
user_signup_schema = UserSignupSchema()