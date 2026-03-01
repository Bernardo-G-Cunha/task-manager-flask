from flask import Blueprint, jsonify, request
from app.auth import admin_required
from app.extensions import limiter
from app.services import get_all_tasks, get_all_users, get_events

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/tasks', methods=["GET"])
@limiter.limit("150 per minute")
@admin_required()
def admin_tasks():

    """
    Admin - List all tasks
    ---
    tags:
      - Admin
    summary: List all tasks (Admin only)
    description: Returns paginated list of all tasks in the system with optional filters.
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Number of items per page
      - name: sort
        in: query
        type: string
        required: false
        default: created_at
        description: Field to sort by
      - name: order
        in: query
        type: string
        enum: [asc, desc]
        required: false
        default: desc
        description: Sort order
      - name: filters
        in: query
        type: string
        required: false
        description: Any additional query parameters will be treated as filters
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
                      deleted_at:
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
      403:
        description: Admin privileges required
    """

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "desc")

    filters = {
        k: v for k, v in request.args.items()
        if k not in {"page", "limit", "sort", "order"}
    }

    result = get_all_tasks(
        page=page,
        limit=limit,
        sort=sort,
        order=order,
        filters=filters
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

@admin_bp.route('/users', methods=["GET"])
@limiter.limit("150 per minute")
@admin_required()
def admin_users():

    """
    Admin - List all users
    ---
    tags:
      - Admin
    summary: List all users (Admin only)
    description: Returns paginated list of all users with optional filters.
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
      - name: sort
        in: query
        type: string
        required: false
        default: username
      - name: order
        in: query
        type: string
        enum: [asc, desc]
        required: false
        default: asc
      - name: filters
        in: query
        type: string
        required: false
        description: Any additional query parameters will be treated as filters
    responses:
      200:
        description: Paginated list of users
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      username:
                        type: string
                      email:
                        type: string
                      role:
                        type: string
                      created_at:
                        type: string
                        format: date-time
                      deleted_at:
                        type: string
                        format: date-time
                      
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
      403:
        description: Admin privileges required
    """

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort = request.args.get("sort", "username")
    order = request.args.get("order", "asc")

    filters = {
        k: v for k, v in request.args.items()
        if k not in {"page", "limit", "sort", "order"}
    }

    result = get_all_users(
        page=page,
        limit=limit,
        sort=sort,
        order=order,
        filters=filters
    )

    return jsonify({
        "success": True,
        "data": {
            "users": result.items
        },
        "pagination": {
            "page": result.page,
            "limit": result.limit,
            "total": result.total,
            "total_pages": result.total_pages
        }
    })

@admin_bp.route('/events', methods=["GET"])
@limiter.limit("150 per minute")
@admin_required()
def admin_list_events():

    """
    Admin - List all events
    ---
    tags:
      - Admin
    summary: List system events (Admin only)
    description: Returns paginated list of system events with optional filters.
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
      - name: sort
        in: query
        type: string
        required: false
        default: username
      - name: order
        in: query
        type: string
        enum: [asc, desc]
        required: false
        default: asc
      - name: filters
        in: query
        type: string
        required: false
        description: Any additional query parameters will be treated as filters
    responses:
      200:
        description: Paginated list of events
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                events:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      entity_type:
                        type: string
                      entity_id:
                        type: integer
                      event_type:
                        type: string
                      actor_user_id:
                        type: integer
                      old_value:
                        type: string
                      new_value:
                        type: string
                      created_at:
                        type: string
                        format: date-time

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
      403:
        description: Admin privileges required
    """

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort = request.args.get("sort", "username")
    order = request.args.get("order", "asc")

    filters = {
        k: v for k, v in request.args.items()
        if k not in {"page", "limit", "sort", "order"}
    }

    result = get_events(
        page=page,
        limit=limit,
        sort=sort,
        order=order,
        filters=filters
    )

    return jsonify({
        "success": True,
        "data": {
            "events": result.items
        },
        "pagination": {
            "page": result.page,
            "limit": result.limit,
            "total": result.total,
            "total_pages": result.total_pages
        }
    })