from app.extensions import db
from app.models.task_tag import tasks_tags  
from app.models.user_tag import users_tags 

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique=True)
    
    tasks = db.relationship('Task', secondary=tasks_tags, back_populates='tags')
    users = db.relationship('User', secondary=users_tags, back_populates='tags')  

    def __repr__(self):
        return f'<Tag id={self.id} name={self.name}>'
