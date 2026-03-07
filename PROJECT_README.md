# Flask Task Management System

A complete Flask learning project: a **Task Management System** with REST API and web UI. Built for interns learning Flask, REST APIs, SQLAlchemy, and JWT authentication.

---

## Project Overview

Users can **register**, **log in**, **create tasks** (title, description, status, priority, due date), and **organize tasks into categories**. The app exposes a **REST API** (JWT-protected) and a **web UI** (session-based) so you can practice both API design and server-rendered pages.

---

## Learning Objectives

By working through this project you will practice:

- **Flask**: Routes, Blueprints, request/response, JSON, templates.
- **HTTP & REST**: GET, POST, PUT, DELETE; status codes 200, 201, 400, 401, 404.
- **Database**: SQLAlchemy ORM, models (User, Task, Category), relationships, queries.
- **Authentication**: JWT for API, sessions for web UI, password hashing (bcrypt).
- **Validation**: Input checks, error messages, protected routes.
- **Structure**: Config, factory pattern, service layer, separation of concerns.

---

## Features

- **Users**: Register, login, view/update profile, change password.
- **Tasks**: Create, read, update, delete; filter by status, priority, category; pagination (API).
- **Categories**: Create, read, update, delete; list tasks in a category (API).
- **Web UI**: Login, register, dashboard, task list/detail/create/edit/delete, category list/create/edit/delete.
- **API**: All operations available as REST endpoints under `/api/auth`, `/api/tasks`, `/api/categories`.

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Steps

1. **Clone or open the project**

   ```bash
   cd task_management_system
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate   # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python run.py
   ```

   The server starts at **http://127.0.0.1:5000**. The first run creates the SQLite database and tables.

5. **Optional: environment variables**

   Create a `.env` file in the project root (do not commit secrets):

   ```
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   DATABASE_URL=sqlite:///task_management.db
   ```

   If not set, the app uses default dev values (see `config.py`).

---

## Commands to Run

| Command            | Description                    |
|--------------------|--------------------------------|
| `python run.py`    | Start the Flask dev server     |
| `pip install -r requirements.txt` | Install dependencies   |

For migrations (optional, if you use Flask-Migrate):

```bash
set FLASK_APP=run.py   # Windows
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## Folder Structure

```
task_management_system/
├── app/
│   ├── __init__.py       # create_app() factory, blueprint registration
│   ├── extensions.py     # db, migrate (shared across app)
│   ├── forms.py          # Flask-WTF forms (login, register, task, category)
│   ├── models/           # User, Task, Category
│   ├── routes/           # auth, tasks, categories, web (UI)
│   ├── services/        # auth_service (register, login, hash, token)
│   ├── utils/            # decorators (JWT), validators, error_handlers
│   ├── templates/        # Jinja2 HTML (base, login, dashboard, tasks, categories)
│   └── static/           # CSS
├── config.py             # Development, Testing, Production config
├── run.py                # Entry point: create app, db.create_all(), run server
├── requirements.txt
├── TUTORIAL.md           # Step-by-step learning guide
├── INTERVIEW_QUESTIONS.md
├── ASSESSMENT.md
└── PROJECT_README.md     # This file
```

---

## How to Test the API

1. **Register**

   ```http
   POST http://127.0.0.1:5000/api/auth/register
   Content-Type: application/json

   {"email": "you@example.com", "password": "yourpassword", "username": "YourName"}
   ```

   Response includes `user` and `token`.

2. **Login**

   ```http
   POST http://127.0.0.1:5000/api/auth/login
   Content-Type: application/json

   {"email": "you@example.com", "password": "yourpassword"}
   ```

   Copy the `token` from the response.

3. **Protected endpoints**

   Add this header to every request:

   ```http
   Authorization: Bearer <your-token>
   ```

   Examples:

   - `GET /api/auth/profile` — current user
   - `GET /api/tasks` — list my tasks (query: `?status=pending&priority=high`)
   - `POST /api/tasks` — create task (JSON body with title, optional description, status, priority, due_date, category_id)
   - `GET /api/tasks/<id>` — one task
   - `PUT /api/tasks/<id>` — update task
   - `DELETE /api/tasks/<id>` — delete task
   - `GET /api/categories` — list my categories
   - `POST /api/categories` — create category (JSON: `{"name": "Work"}`)
   - `GET /api/categories/<id>/tasks` — tasks in that category

Use **Postman** or **curl** to send these requests.

---

## How to Test the UI

1. Open **http://127.0.0.1:5000** in a browser.
2. You are redirected to **Login**. Use **Register** to create an account.
3. After login you see the **Dashboard** (summary and recent tasks).
4. Use **Tasks** to list, create, edit, delete tasks; **Categories** to manage categories.
5. Use **Logout** to clear the session.

---

## Assessment Instructions

- **TUTORIAL.md**: Follow the steps in order; run the app and try each feature.
- **INTERVIEW_QUESTIONS.md**: Use the questions to check your understanding (beginner → scenario).
- **ASSESSMENT.md**: Do the MCQs, coding assignments, debugging tasks, and feature enhancements. Use the evaluation criteria at the end to self-check or get feedback from a mentor.

---

## Common Intern Mistakes

- Forgetting to send `Authorization: Bearer <token>` for API calls to protected routes.
- Filtering tasks or categories by `user_id` so that users only see their own data.
- Storing plain-text passwords instead of hashing with bcrypt.
- Returning 500 or HTML errors instead of consistent JSON and status codes (use error handlers).
- Hardcoding secrets; use environment variables and config classes.

---

## Debugging Tips

- Read the Flask console output and tracebacks.
- Use `print()` or a debugger in routes/services to inspect `request.get_json()`, `current_user`, and query results.
- In Postman, check URL, method, headers (`Content-Type`, `Authorization`), and body.
- Ensure the database file exists and tables are created (`python run.py` runs `db.create_all()` on startup).

---

## What’s Next

After finishing this project:

1. Add tests under `tests/` (e.g. with pytest and pytest-flask).
2. Add search (e.g. by task title) and more filters.
3. Use Flask-Migrate for schema changes.
4. Move on to **Django REST Framework** or **FastAPI** and compare with this Flask design.

Good luck. Focus on understanding concepts; syntax can always be looked up.
