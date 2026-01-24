from app.extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(70), nullable = False)
    description = db.Column(db.Text, nullable = True)
    due_date = db.Column(db.DateTime, nullable = True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False, index=True)

    user = db.relationship('User', back_populates='tasks')
    tags = db.relationship('Tag', secondary='tasks_tags', back_populates='tasks')


    def __repr__(self):
        return f'<Task id={self.id} name={self.name}>'
    