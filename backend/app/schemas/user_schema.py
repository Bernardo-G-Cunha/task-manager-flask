from app.extensions import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    
    tasks = ma.Nested('TaskSchema', many=True)
    tags = ma.Nested('TagSchema', many=True)