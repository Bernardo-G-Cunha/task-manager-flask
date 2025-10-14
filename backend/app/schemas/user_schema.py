from app.extensions import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True, load_only=True)

    tasks = ma.Nested('TaskSchema', many=True)
    tags = ma.Nested('TagSchema', many=True)


user_schema = UserSchema()