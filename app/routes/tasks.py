from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import task_list_schema, task_create_schema, task_update_schema
from app.services import find_task, add_task, update_task, remove_task, get_tasks_paginated
from app.extensions import limiter

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/", methods=["GET"])
@limiter.limit("120 per minute")
@jwt_required()
def list_tasks():

    """
    List user tasks
    ---
    tags:
      - Tasks
    summary: Get all tasks
    description: Returns all tasks belonging to the authenticated user.
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        required: false
      - name: limit
        in: query
        type: integer
        default: 10
        required: false
      - name: sort
        in: query
        type: string
        default: created_at
        required: false
      - name: order
        in: query
        type: string
        default: desc
        enum: [asc, desc]
        required: false
    responses:
      200:
        description: Paginated list of tasks
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                tasks:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      user_id:
                        type: integer
                      name:
                        type: string
                      description:
                        type: string
                      due_date:
                        type: string
                        format: date-time
                      creation_date:
                        type: string
                        format: date-time
                      done:
                        type: boolean
                      tags:
                        type: array
                        items:
                          type: object
            pagination:
              type: object
              properties:
                page:
                  type: integer
                limit:
                  type: integer
                total:
                  type: integer
                total_pages:
                  type: integer
      401:
        description: Unauthorized
      """

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "desc")

    result = get_tasks_paginated(
        user_id=int(get_jwt_identity()),
        page=page,
        limit=limit,
        sort=sort,
        order=order
    )

    return jsonify({
        "success": True,
        "data": {
            "tasks": result.items
        },
        "pagination": {
            "page": result.page,
            "limit": result.limit,
            "total": result.total,
            "total_pages": result.total_pages
        }
    })


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@limiter.limit("120 per minute")
@jwt_required()
def view_task(task_id):

    """
    Get task by ID
    ---
    tags:
      - Tasks
    summary: Get a single task
    description: Returns a specific task belonging to the authenticated user.
    security:
      - BearerAuth: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                task:
                  type: object
                  properties:
                    id:
                      type: integer
                    user_id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    due_date:
                      type: string
                      format: date-time
                    creation_date:
                      type: string
                      format: date-time
                    done:
                      type: boolean
                    tags:
                      type: array
                      items:
                        type: object
                    
      401:
        description: Unauthorized
      404:
        description: Task not found
    """

    user_id = get_jwt_identity()
    taskDTO = find_task(task_id=task_id, user_id=user_id)
    
    return jsonify({"success": True, "data": {"task": taskDTO}}), 200


@tasks_bp.route('/', methods=['POST'])
@limiter.limit("60 per minute")
@jwt_required()
def create_task():

    """
    Create a new task
    ---
    tags:
      - Tasks
    summary: Create a new task
    description: Creates a new task. Only the "name" field is required. All other fields are optional.
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            description:
              type: string
            done:
              type: boolean
            due_date:
              type: string
              format: date-time
            tags:
              type: array
              items:
                type: string  

    responses:
      201:
        description: Task successfully created
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Task successfully created
      400:
        description: Validation error
      401:
        description: Unauthorized
    """

    user_id = get_jwt_identity()
    add_task(task_data=task_create_schema.load(request.get_json()), user_id=user_id)
    
    return jsonify({"success": True, "message": "Task successfully created"}), 201


@tasks_bp.route('/<int:task_id>', methods=['PATCH'])
@limiter.limit("60 per minute")
@jwt_required()
def edit_task(task_id):

    """
    Update task
    ---
    tags:
      - Tasks
    summary: Update a task
    description: Updates one or more fields of an existing task.
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            done:
              type: boolean
            due_date:
              type: string
              format: date-time
            tags:
              type: array
              items:
                type: string
    responses:
      204:
        description: Task successfully updated
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
              example: Task successfully updated
              properties:
                tasks:
                  type: array
                  items:
                    type: object
      400:
        description: Validation error
      401:
        description: Unauthorized
      404:
        description: Task not found
    """

    user_id = get_jwt_identity()    
    update_data = task_update_schema.load(request.get_json())
    
    update_task(update_task_data=update_data, user_id=user_id, task_id=task_id)

    return "", 204


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@limiter.limit("30 per minute")
@jwt_required()
def delete_task(task_id):

    """
    Delete task
    ---
    tags:
      - Tasks
    summary: Delete a task
    description: Soft deletes a task belonging to the authenticated user.
    security:
      - BearerAuth: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      204:
        description: Task successfully deleted
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
              example: Task successfully deleted
              properties:
                tasks:
                  type: array
                  items:
                    type: object
      401:
        description: Unauthorized
      404:
        description: Task not found
    """

    user_id = get_jwt_identity()
    
    remove_task(task_id=task_id, user_id=user_id)

    return "", 204
