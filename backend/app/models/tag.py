from app.extensions import db
from app.models.tasks_tags import tasks_tags  


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    
    tasks = db.relationship('Task', secondary=tasks_tags, back_populate='tags')
    users = db.relationship('User', secondary=tasks_tags, back_populates='tags')    
