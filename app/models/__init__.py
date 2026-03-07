"""
Database models for the Task Management System.
Import db here so models can use it from app.models.
"""
from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app.models.category import Category

__all__ = ["db", "User", "Task", "Category"]
