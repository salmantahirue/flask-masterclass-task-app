"""
Input validation helpers for API requests.
Validates email, password, task fields, category name, etc.
"""
import re
from datetime import datetime


def validate_email(email):
    """Check if email format is valid."""
    if not email or not isinstance(email, str):
        return False, "Email is required"
    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, email


def validate_password(password):
    """Check password length (min 6 for demo; use stronger rules in production)."""
    if not password or not isinstance(password, str):
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, password


def validate_task_data(data):
    """
    Validate task create/update payload.
    Returns (is_valid, cleaned_data or error_message).
    """
    if not data or not isinstance(data, dict):
        return False, "Invalid request body"
    title = (data.get("title") or "").strip()
    if not title:
        return False, "Title is required"
    status = (data.get("status") or "pending").strip().lower()
    if status not in ("pending", "in_progress", "completed"):
        return False, "Status must be pending, in_progress, or completed"
    priority = (data.get("priority") or "medium").strip().lower()
    if priority not in ("low", "medium", "high"):
        return False, "Priority must be low, medium, or high"
    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(data["due_date"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return False, "Invalid due_date format (use ISO format)"
    return True, {
        "title": title,
        "description": (data.get("description") or "").strip(),
        "status": status,
        "priority": priority,
        "due_date": due_date,
        "category_id": data.get("category_id"),
    }


def validate_category_data(data):
    """Validate category name."""
    if not data or not isinstance(data, dict):
        return False, "Invalid request body"
    name = (data.get("name") or "").strip()
    if not name:
        return False, "Category name is required"
    return True, {"name": name}


def validate_profile_data(data):
    """Validate profile update (username only for simplicity)."""
    if not data or not isinstance(data, dict):
        return False, "Invalid request body"
    username = (data.get("username") or "").strip() or None
    return True, {"username": username}
