from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.task_schema import task_list_schema, task_create_schema, task_update_schema
from app.services.tasks import find_task, add_task, update_task, remove_task, get_tasks_paginated

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')

@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def list_tasks():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "desc")

    tasks, total = get_tasks_paginated(
        user_id=int(get_jwt_identity()),
        page=page,
        limit=limit,
        sort=sort,
        order=order
    )

    return jsonify({
        "success": True,
        "data": {
            "tasks": task_list_schema.dump(tasks)
        },
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    })

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def view_task(task_id):
    user_id = get_jwt_identity()
    taskDTO = find_task(task_id=task_id, user_id=user_id)
    
    return jsonify({"success": True, "data": {"task": taskDTO}}), 200


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    add_task(task_data=task_create_schema.load(request.get_json()), user_id=user_id)
    
    return jsonify({"success": True, "message": "Task successfully created"}), 201


@tasks_bp.route('/<int:task_id>', methods=['PATCH'])
@jwt_required()
def edit_task(task_id):
    user_id = get_jwt_identity()    
    update_data = task_update_schema.load(request.get_json())
    
    update_task(update_task_data=update_data, user_id=user_id, task_id=task_id)

    return "", 204



@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    
    remove_task(task_id=task_id, user_id=user_id)

    return "", 204
