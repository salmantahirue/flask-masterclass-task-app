"""
Authentication service: register, login, password hashing, JWT creation.
Business logic lives here; routes only handle HTTP and call services.
"""
import jwt
from datetime import datetime, timedelta
import bcrypt
from flask import current_app
from app.extensions import db
from app.models import User


def hash_password(password):
    """Hash a plain password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password, password_hash):
    """Check if plain password matches hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(user_id):
    """Create a JWT access token for the user."""
    expires = datetime.utcnow() + timedelta(seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    payload = {"user_id": user_id, "exp": expires}
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )


def register_user(email, password, username=None):
    """
    Register a new user. Returns (user, error_message).
    If error_message is not None, registration failed.
    """
    from app.utils.validators import validate_email, validate_password
    ok, result = validate_email(email)
    if not ok:
        return None, result
    email = result
    ok, result = validate_password(password)
    if not ok:
        return None, result
    if User.query.filter_by(email=email).first():
        return None, "Email already registered"
    user = User(
        email=email,
        password_hash=hash_password(password),
        username=username or None,
    )
    db.session.add(user)
    db.session.commit()
    return user, None


def login_user(email, password):
    """
    Authenticate user. Returns (user, error_message).
    If error_message is not None, login failed.
    """
    from app.utils.validators import validate_email
    ok, result = validate_email(email)
    if not ok:
        return None, result
    email = result
    user = User.query.filter_by(email=email).first()
    if not user:
        return None, "Invalid email or password"
    if not check_password(password, user.password_hash):
        return None, "Invalid email or password"
    return user, None
