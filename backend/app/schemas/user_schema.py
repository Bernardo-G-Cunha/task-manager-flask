from app.extensions import ma
from app.models import User
from app.dtos import UserLoginDTO, UserSignupDTO, UserListDTO
from marshmallow import Schema, fields, post_load


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


class UserLoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return UserLoginDTO(**data)


class UserSignupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return UserSignupDTO(**data)


class UserListSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field(required=True)
    
    @post_load
    def make_dto(self, data, **kwargs):
        return UserListDTO(**data)


user_complete_schema = UserCompleteSchema()
user_list_schema = UserListSchema(many=True)
user_login_schema = UserLoginSchema()
user_signup_schema = UserSignupSchema()