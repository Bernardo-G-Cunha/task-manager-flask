from flask import Blueprint, jsonify, request
from app.auth.permissions import admin_required
from app.services.admin import (
    get_all_tasks
)

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/tasks', methods=["GET"])
@admin_required()
def admin_tasks():
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
