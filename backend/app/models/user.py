from app.extensions import db
from app.models.tasks_tags import tasks_tags  

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    
    tasks = db.relationship('Task', back_populate='user')
    
    tags = db.relationship('Tag', secondary=tasks_tags, back_populates='users')