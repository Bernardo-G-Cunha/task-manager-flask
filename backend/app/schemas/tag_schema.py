from app.models import Tag
from app.extensions import ma

class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tag
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)

    tasks = ma.Nested('TaskSchema', many=True)
    user = ma.Nested('UserSchema', many=True)