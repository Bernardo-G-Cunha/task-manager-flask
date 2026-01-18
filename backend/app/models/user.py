from app.extensions import db
from app.models.user_tag import users_tags 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)

    tasks = db.relationship('Task', back_populates='user')
    tags = db.relationship('Tag', secondary=users_tags, back_populates='users')
    
    def __repr__(self):
        return f'<User id={self.id} name={self.username} email={self.email}>'
