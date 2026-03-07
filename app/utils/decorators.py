"""
Decorators for protecting routes (JWT authentication).
Use @token_required on a route to require a valid JWT in the Authorization header.
"""
import jwt
from functools import wraps
from flask import request, current_app, jsonify
from app.extensions import db
from app.models import User


def token_required(f):
    """
    Decorator that checks for a valid JWT in the Authorization header.
    Injects the current user into the route as keyword arg 'current_user'.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 401
            kwargs["current_user"] = user
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
    return decorated
