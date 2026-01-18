from app.extensions import ma
from app.models.user import User
from app.dtos.dto_user import UserLoginDTO, UserSignupDTO
from marshmallow import Schema, fields, post_load

# Complete schema to keep and return data
class UserCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True, load_only=True)

    tasks = ma.Nested("TaskCompleteSchema", many=True)
    tags = ma.Nested("TagSchema", many=True)


# Login only schema
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return UserLoginDTO(**data)

# Signup only schema
class UserSignupSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return UserSignupDTO(**data)
    
user_complete_schema = UserCompleteSchema()
user_login_schema = UserLoginSchema()
user_signup_schema = UserSignupSchema()