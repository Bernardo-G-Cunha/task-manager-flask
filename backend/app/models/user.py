from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique=True)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), nullable=False, default="USER")

    tasks = db.relationship('Task', back_populates='user')
    tags = db.relationship('Tag', secondary="users_tags", back_populates='users')
    
    def __repr__(self):
        return f'<User id={self.id} name={self.username} email={self.email}>'
