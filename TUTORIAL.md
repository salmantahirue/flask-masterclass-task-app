# Flask Task Management System — Step-by-Step Tutorial

This tutorial teaches Flask using a **Task Management System**. You will build an app where users register, log in, create tasks, and organize them into categories. Every step explains the concept, why it is needed, and how it connects to the project.

---

## 1. Project Overview

### Problem Statement

Teams and individuals need a place to track work: what to do, when it is due, and whether it is done. A **Task Management System** lets users:

- Create an account and log in
- Add tasks (title, description, status, priority, due date)
- Group tasks into categories (e.g. Work, Personal)
- Filter and view tasks by status or priority

### Real-Life Examples

- **Company**: Interns get tasks like "Complete API documentation" or "Fix login bug" with due dates and priorities.
- **Personal**: "Buy groceries", "Call dentist" with status (pending / in progress / completed).
- **Learning**: Your own study tasks (e.g. "Finish Flask tutorial", "Build Task API") with categories like "Flask", "Database".

### Why Flask?

- **Minimal**: You see how HTTP, routes, and responses work without too much magic.
- **Flexible**: You choose how to structure code, which libraries to use, and how to organize routes.
- **Foundation**: After Flask, Django REST Framework and FastAPI are easier to learn.

### How This Project Teaches Flask

- **HTTP & REST**: You use GET, POST, PUT, DELETE and status codes (200, 201, 400, 401, 404).
- **Routes & Blueprints**: URLs map to functions; blueprints group auth, tasks, and categories.
- **Database & ORM**: User, Task, and Category models with SQLAlchemy and relationships.
- **Authentication**: JWT for the API; sessions for the web UI.
- **Validation & Errors**: Input checks and consistent error responses.

---

## 2. Learning Flow (Step-by-Step)

### Step 1: Flask Introduction & Environment Setup

**Concept**: A web app needs a Python environment and Flask installed so the server can handle HTTP requests.

**Why**: Without Flask, you would have to parse HTTP and manage URLs by hand. Flask does that for you.

**What you do**:

```bash
# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**In the project**: `requirements.txt` lists Flask, SQLAlchemy, PyJWT, bcrypt, etc. Running `python run.py` starts the app and creates the database tables.

---

### Step 2: Project Structure & Configuration

**Concept**: Code is split into **config**, **app** (models, routes, utils), and **entry point** so the app is easy to run and test in different environments.

**Why**: One place for database URL and secrets (config), one place for "create the app" (factory), and clear folders for models, routes, and helpers.

**Structure**:

```
task_management_system/
  config.py          # Settings (dev/test/prod)
  run.py             # Entry point: create app, run server
  app/
    __init__.py      # create_app() factory
    extensions.py    # db, migrate (avoids circular imports)
    forms.py         # Flask-WTF forms for web UI
    models/          # User, Task, Category
    routes/          # auth, tasks, categories, web
    services/        # auth_service (register, login, hash)
    utils/           # decorators (JWT), validators, error_handlers
    templates/       # HTML (Jinja2)
    static/          # CSS
  tests/
```

**In the project**: `config.py` has `DevelopmentConfig` (SQLite, DEBUG=True). `create_app("development")` in `run.py` uses that config.

---

### Step 3: Routing & Views

**Concept**: A **route** maps a URL and HTTP method to a Python function. That function returns a response (e.g. JSON or HTML).

**Why**: The client asks for `/api/tasks` or `/login`; Flask calls the right function and sends back data or a page.

**Example** (from `app/routes/auth.py`):

```python
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user, err = login_user(data.get("email"), data.get("password"))
    if err:
        return jsonify({"error": err}), 401
    token = create_token(user.id)
    return jsonify({"user": user.to_dict(), "token": token}), 200
```

**Task Management**: `/api/auth/login` receives email and password, checks them, and returns the user and a JWT.

---

### Step 4: Templates & Jinja2

**Concept**: **Jinja2** is Flask’s template engine. You write HTML with placeholders (`{{ variable }}`) and blocks (`{% block content %}`) so the server can inject data and reuse layout.

**Why**: You don’t build HTML strings in Python. You keep layout (e.g. `base.html`) once and only fill in the changing parts (e.g. task list, login form).

**Example** (from `app/templates/base.html`):

```html
<nav>
  {% if current_user %}
    <a href="{{ url_for('web.dashboard') }}">Dashboard</a>
    <a href="{{ url_for('web.logout') }}">Logout</a>
  {% else %}
    <a href="{{ url_for('web.login') }}">Login</a>
  {% endif %}
</nav>
<main>{% block content %}{% endblock %}</main>
```

**Task Management**: The dashboard extends `base.html` and fills `content` with summary cards and recent tasks.

---

### Step 5: Forms & Validation (Flask-WTF)

**Concept**: **Flask-WTF** gives you form classes (e.g. `LoginForm`, `TaskForm`) with validation. You render them in templates and handle POST in the route.

**Why**: You avoid manual checks for "email required", "password length", etc. The form class validates and shows errors.

**Example** (from `app/forms.py` and `app/templates/login.html`):

```python
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
```

```html
<form method="post">
  {{ form.hidden_tag() }}
  {{ form.email.label }} {{ form.email() }}
  {{ form.password.label }} {{ form.password() }}
  <button type="submit">Login</button>
</form>
```

**Task Management**: Login, register, create/edit task, and create/edit category all use Flask-WTF forms in the web UI.

---

### Step 6: Database & ORM (SQLAlchemy)

**Concept**: **ORM** (Object-Relational Mapping) lets you work with tables as Python classes. You define **models** (e.g. `User`, `Task`), set **relationships** (user has many tasks), and use **sessions** to add/query/commit.

**Why**: You write Python instead of raw SQL, and the ORM handles queries and relationships.

**Example** (from `app/models/task.py`):

```python
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
```

**Task Management**: User has many Tasks and many Categories. Task belongs to one User and optionally one Category. This matches "my tasks" and "my categories".

---

### Step 7: User Authentication & Authorization

**Concept**: **Authentication** = "who are you?" (login). **Authorization** = "what can you do?" (e.g. only your tasks). Here we use **JWT** for the API and **sessions** for the browser.

**Why**: The API needs a token (JWT) in the `Authorization` header. The web UI needs a simple "logged in" state (session) so we can show dashboard and task pages.

**Example** (from `app/utils/decorators.py`):

```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user = db.session.get(User, payload["user_id"])
        kwargs["current_user"] = user
        return f(*args, **kwargs)
    return decorated
```

**Task Management**: API routes for tasks and categories use `@token_required` so only the owner can see or change their data. Web routes use `@login_required` and `session["user_id"]`.

---

### Step 8: Blueprints

**Concept**: A **Blueprint** is a set of routes (and optional templates/static) that you register on the app. It keeps auth, tasks, categories, and web UI in separate modules.

**Why**: One file per "feature" (auth, tasks, categories, web) instead of one giant `routes.py`.

**Example** (from `app/__init__.py`):

```python
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.routes.categories import categories_bp
from app.routes.web import web_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
app.register_blueprint(categories_bp, url_prefix="/api/categories")
app.register_blueprint(web_bp)
```

**Task Management**: All auth endpoints live under `/api/auth`, tasks under `/api/tasks`, categories under `/api/categories`, and web pages (login, dashboard, etc.) under `/` without a prefix.

---

### Step 9: CRUD Operations for Tasks

**Concept**: **CRUD** = Create, Read, Update, Delete. For tasks you need: create task, list my tasks, get one task, update task, delete task. Each operation uses the right HTTP method and status code.

**Why**: REST APIs follow this pattern so clients (and developers) know what to expect.

**In the project**:

- **Create**: `POST /api/tasks` → validate body, create `Task`, return 201.
- **Read list**: `GET /api/tasks` → filter by `user_id`, optional status/priority/category, paginate, return 200.
- **Read one**: `GET /api/tasks/<id>` → return 200 if owned by current user, else 404.
- **Update**: `PUT /api/tasks/<id>` → validate body, update fields, return 200.
- **Delete**: `DELETE /api/tasks/<id>` → delete if owned, return 200.

Same idea applies to categories (and user profile in auth).

---

### Step 10: REST APIs

**Concept**: **REST** means resources (users, tasks, categories) are identified by URLs, and actions are expressed with HTTP methods and status codes. Responses are usually JSON.

**Why**: Other apps (mobile, frontend, scripts) can use the same API in a standard way.

**Conventions used in this project**:

- **URLs**: Nouns, plural (`/api/tasks`, `/api/categories`).
- **Methods**: GET (read), POST (create), PUT (update), DELETE (delete).
- **Status codes**: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable.
- **Auth**: `Authorization: Bearer <token>` for protected endpoints.

**Task Management**: Every requirement from the README (register, login, profile, tasks CRUD, categories CRUD, filters) is implemented as REST endpoints under `/api/auth`, `/api/tasks`, `/api/categories`.

---

### Step 11: Error Handling & Logging

**Concept**: **Error handlers** catch exceptions and return a consistent JSON (or page) so the client always gets a clear message and status code.

**Why**: Without handlers, a 500 might leak stack traces or return HTML. With handlers, you return `{"error": "Not found"}` and 404.

**Example** (from `app/utils/error_handlers.py`):

```python
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found", "message": "Resource not found"}), 404
```

**Task Management**: 400 for validation errors, 401 for missing/invalid token, 404 for task/category not found or not owned.

---

### Step 12: Testing

**Concept**: **Tests** call your routes (and services) with fake data and assert the response status and body. You run them with `pytest`.

**Why**: You can change code and re-run tests to make sure login, task CRUD, and auth still work.

**Example** (you can add under `tests/`):

```python
def test_register(client):
    r = client.post("/api/auth/register", json={"email": "a@b.com", "password": "secret12"})
    assert r.status_code == 201
    assert "token" in r.json()
```

**Task Management**: You can add tests for register, login, create task, get tasks, update task, delete task, and for "cannot access another user’s task".

---

### Step 13: Deployment Basics

**Concept**: **Deployment** means running the app on a server with a real database and HTTPS. You use environment variables for `SECRET_KEY`, `JWT_SECRET_KEY`, and `DATABASE_URL`, and turn off `DEBUG`.

**Why**: Development uses SQLite and DEBUG; production uses PostgreSQL (or similar) and no DEBUG.

**Task Management**: The same `create_app()` and config classes support `development` and `production`. You set `FLASK_ENV=production` and `DATABASE_URL` and run with a production WSGI server (e.g. Gunicorn).

---

## 3. Design Patterns & Best Practices

- **MVC-style**: Models (User, Task, Category), Views (templates + routes), and control flow in routes and services.
- **Blueprint pattern**: One blueprint per feature (auth, tasks, categories, web).
- **Service layer**: `auth_service.register_user`, `login_user`; routes only do HTTP and call services.
- **Factory pattern**: `create_app(config_name)` so one codebase can run in dev/test/prod.
- **Separation of concerns**: Routes handle request/response; services handle business logic; models handle data; validators handle input.
- **Environment-based config**: `config.py` and `config_by_name`; secrets and DB URL from environment.
- **Naming**: Clear names (`token_required`, `validate_task_data`, `auth_bp`, `tasks_bp`).

---

## 4. How Frontend Connects to Backend

- **Web UI (browser)**:
  - User opens `/login` or `/register`. Flask renders the form (Jinja2).
  - On submit, the form POSTs to the same URL. The route calls `login_user` or `register_user`, sets `session["user_id"]`, and redirects to `/dashboard`.
  - Dashboard and task list routes use `@login_required` and read tasks from the database, then render templates with that data.
- **REST API** (Postman, another app):
  - Client POSTs to `/api/auth/login` with JSON `{ "email", "password" }`. Response includes `token`.
  - Client sends `Authorization: Bearer <token>` on every request to `/api/tasks`, `/api/categories`. The `@token_required` decorator loads the user and passes `current_user` into the route.

---

## 5. Database Design (Simple Explanation)

- **User**: id, email, password_hash, username, timestamps. One user has many tasks and many categories.
- **Task**: id, title, description, status, priority, due_date, user_id, category_id, timestamps. Each task belongs to one user and optionally one category.
- **Category**: id, name, user_id, timestamps. Each category belongs to one user and has many tasks.

Relationships: User → Tasks (one-to-many), User → Categories (one-to-many), Category → Tasks (one-to-many). So "my tasks" and "my categories" are simple filters by `user_id`.

---

## 6. What to Do Next

1. Run the app: `python run.py`, open http://127.0.0.1:5000, register and create tasks.
2. Test the API with Postman: login, copy the token, then call GET/POST/PUT/DELETE on `/api/tasks` and `/api/categories` with the header `Authorization: Bearer <token>`.
3. Read one route at a time (e.g. `app/routes/tasks.py`) and match it to the steps above.
4. Add a small feature (e.g. search tasks by title) and write a test for it.

This project is your **complete Flask learning roadmap**: from setup and routing to database, auth, REST API, and a simple web UI, all in one Task Management System.
