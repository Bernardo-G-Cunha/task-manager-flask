from flask import Blueprint, request, make_response, redirect, url_for, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.task_schema import *
from app.models import Task

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')


@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
        
    return jsonify(tasks=task_list_schema.dump(tasks))
        
@tasks_bp.route('/view', methods=['GET'])
@jwt_required()
def view_task():
    user_id = get_jwt_identity()
    task = Task.query.filter_by().all()
    
    return

@tasks_bp.route('/create', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = task_schema.load(request.get_json())
    new_task = Task(**data, user_id=user_id)

    new_task.save()

    return jsonify(message="Task successfully created"), 201

@tasks_bp.route('/edit', methods=['PUT'])
@jwt_required()
def edit_task():
    user_id = get_jwt_identity()
    



    return jsonify()
