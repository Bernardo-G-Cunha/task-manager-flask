from app.models import Task
from app.extensions import ma

class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    due = ma.auto_field()
    creation_date = ma.auto_field()

    tags = ma.Nested('TagSchema', many=True)
