# app/schemas/event_schema.py
from app.models import Event
from app.extensions import ma
from app.dtos import EventDTO
from marshmallow import post_dump

class EventSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Event

    id = ma.auto_field(dump_only=True)

    entity_type = ma.auto_field()
    entity_id = ma.auto_field()

    event_type = ma.auto_field()

    actor_user_id = ma.auto_field(allow_none=True)

    old_value = ma.auto_field(allow_none=True)
    new_value = ma.auto_field(allow_none=True)

    created_at = ma.auto_field(
        format="iso",
        dump_only=True
    )

    @post_dump
    def make_dto(self, data, **kwargs):
        return EventDTO(**data)


event_schema = EventSchema()
event_list_schema = EventSchema(many=True)
