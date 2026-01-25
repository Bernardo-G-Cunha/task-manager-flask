from app.extensions import db

tasks_tags = db.Table(
    'tasks_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id', ondelete="CASCADE"), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)