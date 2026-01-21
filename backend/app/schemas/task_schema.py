from app.models import Task
from app.extensions import ma
from app.dtos.dto_task import TaskCreateDTO, TaskUpdateDTO
from marshmallow import post_load

class TaskCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    description = ma.auto_field()
    due_date = ma.auto_field()
    done = ma.auto_field()
    creation_date = ma.auto_field(format='iso', dump_only=True, allow_none=True)

    tags = ma.Nested("TagSchema", many=True)


class TaskCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True

    name = ma.auto_field(required=True)
    description = ma.auto_field()
    due_date = ma.auto_field()
    done = ma.auto_field()
    
    tags = ma.Nested("TagSchema", many=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return TaskCreateDTO(**data)

class TaskUpdateSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Task
        load_instance = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    due_date = ma.auto_field()
    done = ma.auto_field()
    
    tags = ma.Nested("TagSchema", many=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return TaskUpdateDTO(**data)
    
   

task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()
task_list_schema = TaskCompleteSchema(many=True)