"""
Authentication API routes: register, login, profile.
REST: POST /register, POST /login, GET /profile, PUT /profile.
"""
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from app.services.auth_service import register_user, login_user, create_token, hash_password
from app.utils.decorators import token_required
from app.utils.validators import validate_email, validate_password, validate_profile_data

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Body: { "email": "...", "password": "...", "username": "..." (optional) }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    user, err = register_user(email, password, username)
    if err:
        return jsonify({"error": err}), 400
    token = create_token(user.id)
    return jsonify({"user": user.to_dict(), "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user. Returns user and JWT token.
    Body: { "email": "...", "password": "..." }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    user, err = login_user(email, password)
    if err:
        return jsonify({"error": err}), 401
    token = create_token(user.id)
    return jsonify({"user": user.to_dict(), "token": token}), 200


@auth_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    """Get current user profile (protected)."""
    return jsonify(current_user.to_dict()), 200


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """
    Update current user profile (e.g. username).
    Body: { "username": "..." }
    """
    data = request.get_json(silent=True) or {}
    ok, result = validate_profile_data(data)
    if not ok:
        return jsonify({"error": result}), 400
    current_user.username = result.get("username")
    db.session.commit()
    return jsonify(current_user.to_dict()), 200


@auth_bp.route("/change-password", methods=["PUT"])
@token_required
def change_password(current_user):
    """
    Change password.
    Body: { "current_password": "...", "new_password": "..." }
    """
    from app.services.auth_service import check_password
    data = request.get_json(silent=True) or {}
    current_pw = data.get("current_password")
    new_pw = data.get("new_password")
    if not current_pw or not new_pw:
        return jsonify({"error": "current_password and new_password required"}), 400
    if not check_password(current_pw, current_user.password_hash):
        return jsonify({"error": "Current password is wrong"}), 401
    ok, msg = validate_password(new_pw)
    if not ok:
        return jsonify({"error": msg}), 400
    current_user.password_hash = hash_password(new_pw)
    db.session.commit()
    return jsonify({"message": "Password updated"}), 200
