from app.extensions import db
from app.models.tasks_tags import tasks_tags  

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(70), nullable = False)
    description = db.Column(db.Text, nullable = True)
    due = db.Column(db.DateTime, nullable = True)
    creation_date = db.Column(db.DateTime, nullable = False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populate='tasks')
    tags = db.relationship('Tag', secondary=tasks_tags, back_populate='tasks')


    def __repr__(self):
        return f'<Task id={self.id} name={self.name}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




"""
                <p class="task_name">Task name</p>
                <p class="task_class">Task class</p>
                <p class="task_group">Task group</p>
                <p class="task_description">Task description</p>
                <p class="task_due">Task due date</p>
                <p class="task_creation">Task creation date</p>
"""