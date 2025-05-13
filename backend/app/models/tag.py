from app.extensions import db
from app.models.tasks_tags import tasks_tags  


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    
    tasks = db.relationship('Task', secondary=tasks_tags, back_populate='tags')
    users = db.relationship('User', secondary=tasks_tags, back_populates='tags')    

    def __repr__(self):
        return f'<Tag id={self.id} name={self.name}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

