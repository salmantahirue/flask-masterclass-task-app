"""
Category API routes: CRUD for categories.
REST: GET/POST /categories, GET/PUT/DELETE /categories/<id>, GET /categories/<id>/tasks
"""
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Category, Task
from app.utils.decorators import token_required
from app.utils.validators import validate_category_data

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("", methods=["GET"])
@token_required
def list_categories(current_user):
    """Get all categories for the current user."""
    cats = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return jsonify({"categories": [c.to_dict() for c in cats]}), 200


@categories_bp.route("", methods=["POST"])
@token_required
def create_category(current_user):
    """Create a new category. Body: { "name": "..." }"""
    data = request.get_json(silent=True) or {}
    ok, result = validate_category_data(data)
    if not ok:
        return jsonify({"error": result}), 400
    cat = Category(name=result["name"], user_id=current_user.id)
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201


@categories_bp.route("/<int:category_id>", methods=["GET"])
@token_required
def get_category(current_user, category_id):
    """Get a single category (only if owned by current user)."""
    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(cat.to_dict()), 200


@categories_bp.route("/<int:category_id>", methods=["PUT"])
@token_required
def update_category(current_user, category_id):
    """Update a category (only if owned by current user)."""
    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "Category not found"}), 404
    data = request.get_json(silent=True) or {}
    ok, result = validate_category_data(data)
    if not ok:
        return jsonify({"error": result}), 400
    cat.name = result["name"]
    db.session.commit()
    return jsonify(cat.to_dict()), 200


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@token_required
def delete_category(current_user, category_id):
    """Delete a category. Tasks in this category will have category_id set to None."""
    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "Category not found"}), 404
    # Unlink tasks from this category instead of deleting them
    Task.query.filter_by(category_id=category_id).update({"category_id": None})
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


@categories_bp.route("/<int:category_id>/tasks", methods=["GET"])
@token_required
def list_category_tasks(current_user, category_id):
    """Get all tasks in a category (only if category owned by current user)."""
    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "Category not found"}), 404
    tasks = Task.query.filter_by(user_id=current_user.id, category_id=category_id).order_by(Task.created_at.desc()).all()
    return jsonify({"tasks": [t.to_dict() for t in tasks]}), 200
