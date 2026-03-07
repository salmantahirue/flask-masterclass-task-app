"""
Task API routes: CRUD for tasks.
REST: GET/POST /tasks, GET/PUT/DELETE /tasks/<id>
Filter by status, priority, due_date. Pagination optional.
"""
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Task
from app.utils.decorators import token_required
from app.utils.validators import validate_task_data

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["GET"])
@token_required
def list_tasks(current_user):
    """
    Get all tasks for the current user.
    Query params: status, priority, category_id, page, per_page
    """
    q = Task.query.filter_by(user_id=current_user.id)
    status = request.args.get("status")
    if status:
        q = q.filter(Task.status == status)
    priority = request.args.get("priority")
    if priority:
        q = q.filter(Task.priority == priority)
    category_id = request.args.get("category_id")
    if category_id:
        q = q.filter(Task.category_id == int(category_id))
    q = q.order_by(Task.created_at.desc())
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    items = [t.to_dict() for t in pagination.items]
    return jsonify({"tasks": items, "total": pagination.total, "page": page, "per_page": per_page}), 200


@tasks_bp.route("", methods=["POST"])
@token_required
def create_task(current_user):
    """
    Create a new task.
    Body: { "title": "...", "description": "...", "status": "pending", "priority": "medium", "due_date": "...", "category_id": 1 }
    """
    data = request.get_json(silent=True) or {}
    ok, result = validate_task_data(data)
    if not ok:
        return jsonify({"error": result}), 400
    task = Task(
        title=result["title"],
        description=result["description"] or None,
        status=result["status"],
        priority=result["priority"],
        due_date=result["due_date"],
        category_id=result.get("category_id"),
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@token_required
def get_task(current_user, task_id):
    """Get a single task by id (only if owned by current user)."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
    """Update a task (only if owned by current user)."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json(silent=True) or {}
    ok, result = validate_task_data(data)
    if not ok:
        return jsonify({"error": result}), 400
    task.title = result["title"]
    task.description = result["description"] or None
    task.status = result["status"]
    task.priority = result["priority"]
    task.due_date = result["due_date"]
    task.category_id = result.get("category_id")
    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
    """Delete a task (only if owned by current user)."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
