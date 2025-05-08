from app.extensions import db
from app.models.tasks_tags import tasks_tags  

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    tag = db.Column(db.String, nullable = True) #Adicional foreign key e revisar
    description = db.Column(db.String, nullable = True)
    due = db.Column(db.Date, nullable = True)
    creation_date = db.Column(db.Date, nullable = False)

    user = db.relationship('User', back_populate='tasks')
    tags = db.relationship('Tag', secondary=tasks_tags, back_populate='tasks')



"""
                <p class="task_name">Task name</p>
                <p class="task_class">Task class</p>
                <p class="task_group">Task group</p>
                <p class="task_description">Task description</p>
                <p class="task_due">Task due date</p>
                <p class="task_creation">Task creation date</p>
"""