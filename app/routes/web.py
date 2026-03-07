"""
Web UI routes: login, register, dashboard, tasks, categories.
Uses Flask session for browser auth (simpler for interns). API uses JWT.
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from app.extensions import db
from app.models import User, Task, Category
from app.forms import LoginForm, RegisterForm, TaskForm, CategoryForm
from app.services.auth_service import register_user, login_user, hash_password
from app.utils.validators import validate_task_data, validate_category_data

web_bp = Blueprint("web", __name__)


def login_required(f):
    """Require user to be logged in (session)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("web.login"))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    """Get current user from session."""
    if "user_id" not in session:
        return None
    return db.session.get(User, session["user_id"])


@web_bp.route("/")
def index():
    """Home: redirect to dashboard if logged in, else login."""
    if "user_id" in session:
        return redirect(url_for("web.dashboard"))
    return redirect(url_for("web.login"))


@web_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    if "user_id" in session:
        return redirect(url_for("web.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user, err = login_user(form.email.data, form.password.data)
        if err:
            flash(err, "danger")
            return render_template("login.html", form=form)
        session["user_id"] = user.id
        flash(f"Welcome back, {user.username or user.email}!", "success")
        return redirect(url_for("web.dashboard"))
    return render_template("login.html", form=form)


@web_bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration page."""
    if "user_id" in session:
        return redirect(url_for("web.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        user, err = register_user(form.email.data, form.password.data, form.username.data)
        if err:
            flash(err, "danger")
            return render_template("register.html", form=form)
        session["user_id"] = user.id
        flash("Account created. Welcome!", "success")
        return redirect(url_for("web.dashboard"))
    return render_template("register.html", form=form)


@web_bp.route("/logout")
def logout():
    """Logout and clear session."""
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("web.login"))


@web_bp.route("/dashboard")
@login_required
def dashboard():
    """Task dashboard: list tasks and summary."""
    user = get_current_user()
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.updated_at.desc()).limit(20).all()
    pending = Task.query.filter_by(user_id=user.id, status="pending").count()
    completed = Task.query.filter_by(user_id=user.id, status="completed").count()
    return render_template(
        "dashboard.html",
        user=user,
        tasks=tasks,
        pending_count=pending,
        completed_count=completed,
    )


@web_bp.route("/tasks")
@login_required
def task_list():
    """List all tasks with optional filters."""
    user = get_current_user()
    q = Task.query.filter_by(user_id=user.id)
    status = request.args.get("status")
    if status:
        q = q.filter(Task.status == status)
    priority = request.args.get("priority")
    if priority:
        q = q.filter(Task.priority == priority)
    category_id = request.args.get("category_id", type=int)
    if category_id:
        q = q.filter(Task.category_id == category_id)
    tasks = q.order_by(Task.created_at.desc()).all()
    categories = Category.query.filter_by(user_id=user.id).order_by(Category.name).all()
    return render_template("tasks/list.html", tasks=tasks, categories=categories, user=user)


@web_bp.route("/tasks/new", methods=["GET", "POST"])
@login_required
def task_new():
    """Create a new task."""
    user = get_current_user()
    form = TaskForm()
    form.category_id.choices = [(0, "-- No category --")] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=user.id).order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data or None,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=form.category_id.data if form.category_id.data else None,
            user_id=user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created.", "success")
        return redirect(url_for("web.task_list"))
    return render_template("tasks/form.html", form=form, task=None, title="New Task")


@web_bp.route("/tasks/<int:task_id>")
@login_required
def task_detail(task_id):
    """View a single task."""
    user = get_current_user()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for("web.task_list"))
    return render_template("tasks/detail.html", task=task, user=user)


@web_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def task_edit(task_id):
    """Edit a task."""
    user = get_current_user()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for("web.task_list"))
    form = TaskForm(obj=task)
    form.category_id.choices = [(0, "-- No category --")] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=user.id).order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data or None
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.category_id = form.category_id.data if form.category_id.data else None
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("web.task_detail", task_id=task.id))
    form.status.data = task.status
    form.priority.data = task.priority
    form.category_id.data = task.category_id or 0
    return render_template("tasks/form.html", form=form, task=task, title="Edit Task")


@web_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    """Delete a task."""
    user = get_current_user()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for("web.task_list"))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("web.task_list"))


@web_bp.route("/categories")
@login_required
def category_list():
    """List categories."""
    user = get_current_user()
    categories = Category.query.filter_by(user_id=user.id).order_by(Category.name).all()
    return render_template("categories/list.html", categories=categories, user=user)


@web_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def category_new():
    """Create a category."""
    user = get_current_user()
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(name=form.name.data, user_id=user.id)
        db.session.add(cat)
        db.session.commit()
        flash("Category created.", "success")
        return redirect(url_for("web.category_list"))
    return render_template("categories/form.html", form=form, category=None, title="New Category")


@web_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def category_edit(category_id):
    """Edit a category."""
    user = get_current_user()
    cat = Category.query.filter_by(id=category_id, user_id=user.id).first()
    if not cat:
        flash("Category not found.", "danger")
        return redirect(url_for("web.category_list"))
    form = CategoryForm(obj=cat)
    if form.validate_on_submit():
        cat.name = form.name.data
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("web.category_list"))
    return render_template("categories/form.html", form=form, category=cat, title="Edit Category")


@web_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def category_delete(category_id):
    """Delete a category."""
    user = get_current_user()
    cat = Category.query.filter_by(id=category_id, user_id=user.id).first()
    if not cat:
        flash("Category not found.", "danger")
        return redirect(url_for("web.category_list"))
    Task.query.filter_by(category_id=category_id).update({"category_id": None})
    db.session.delete(cat)
    db.session.commit()
    flash("Category deleted.", "success")
    return redirect(url_for("web.category_list"))
