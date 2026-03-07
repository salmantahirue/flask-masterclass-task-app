# Flask Task Management System

A **complete Flask learning project** for Python interns: a **Task Management System** with REST API and web UI. Built strictly from the requirements in the parent [README](../README.md). Use it to learn Flask, HTTP, REST, SQLAlchemy, JWT, and clean architecture step by step.

---

## 1. Project Overview

### Problem Statement

Teams and individuals need a place to track work: what to do, when it is due, and whether it is done. A **Task Management System** lets users:

- Create an account and log in
- Add tasks (title, description, status, priority, due date)
- Group tasks into categories (e.g. Work, Personal)
- Filter and view tasks by status or priority
- See only their own tasks and categories

### Real-Life Examples

- **Company:** Interns get tasks like “Complete API documentation” or “Fix login bug” with due dates and priorities.
- **Personal:** “Buy groceries”, “Call dentist” with status (pending / in progress / completed).
- **Learning:** Your own study tasks (e.g. “Finish Flask tutorial”, “Build Task API”) with categories like “Flask”, “Database”.

### Why Flask?

- **Minimal:** You see how HTTP, routes, and responses work without too much magic.
- **Flexible:** You choose how to structure code and which libraries to use.
- **Foundation:** After Flask, Django REST Framework and FastAPI are easier to learn.

### How This Project Helps You Learn

- **HTTP & REST:** GET, POST, PUT, DELETE; status codes 200, 201, 400, 401, 404.
- **Flask:** Routes, Blueprints, request/response, JSON, templates, error handlers.
- **Database:** SQLAlchemy ORM, models (User, Task, Category), relationships, queries.
- **Authentication:** JWT for the API; sessions for the web UI; password hashing.
- **Validation & Errors:** Input checks and consistent JSON error responses.
- **Structure:** Config, factory pattern, service layer, separation of concerns.

---

## 2. Learning Objectives

By working through this project you will practice:

| Area | What you learn |
|------|----------------|
| **Flask** | Routes, Blueprints, request/response, JSON, Jinja2 templates |
| **HTTP & REST** | Methods, status codes, RESTful URLs, stateless API |
| **Database** | SQLAlchemy models, relationships (one-to-many), queries, filters |
| **Authentication** | JWT for API, sessions for web UI, password hashing (bcrypt) |
| **Validation** | Input checks, error messages, protected routes |
| **Architecture** | Config, factory pattern, service layer, separation of concerns |

---

## 3. Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Steps

1. **Open the project folder**

   ```bash
   cd task_management_system
   ```

2. **Create and activate a virtual environment**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux / Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
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

   If not set, the app uses default dev values from `config.py`.

---

## 4. Features List

### Users

- Register with email and password
- Login and get JWT token (API) or session (web UI)
- View and update profile
- Change password (API)

### Tasks

- Create, read, update, delete tasks
- Each task has: title, description, status (pending / in progress / completed), priority (low / medium / high), due date
- Filter by status, priority, category; pagination (API)
- Users see only their own tasks

### Categories

- Create, read, update, delete categories
- Assign tasks to categories
- List tasks in a category (API)
- Users see only their own categories

### Web UI

- Login and registration pages
- Dashboard (summary and recent tasks)
- Task list, create/edit task, task detail, delete task
- Category list, create/edit category, delete category
- Session-based auth; logout

### REST API

- All operations under `/api/auth`, `/api/tasks`, `/api/categories`
- JWT in `Authorization: Bearer <token>` for protected endpoints
- JSON request/response; consistent error format and status codes

---

## 5. Folder Structure and Purpose

Every folder and key file is explained so you know where to look when learning or changing code.

```
task_management_system/
│
├── app/                          # Main application package
│   ├── __init__.py               # create_app() factory; registers blueprints and error handlers
│   ├── config.py                 # (Optional) re-export; main config is in project root config.py
│   ├── extensions.py             # Shared extensions: db (SQLAlchemy), migrate (Flask-Migrate)
│   ├── forms.py                  # Flask-WTF forms: Login, Register, Task, Category
│   │
│   ├── models/                   # Database models (ORM)
│   │   ├── __init__.py           # Exports db, User, Task, Category
│   │   ├── user.py               # User model: id, email, password_hash, username, timestamps
│   │   ├── task.py               # Task model: title, description, status, priority, due_date, user_id, category_id
│   │   └── category.py           # Category model: name, user_id
│   │
│   ├── routes/                   # API and web routes (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py               # API: register, login, profile, change-password
│   │   ├── tasks.py              # API: CRUD tasks, filters, pagination
│   │   ├── categories.py         # API: CRUD categories, list tasks in category
│   │   └── web.py                # Web UI: login, register, dashboard, tasks, categories (session auth)
│   │
│   ├── services/                 # Business logic (no HTTP here)
│   │   ├── __init__.py
│   │   └── auth_service.py       # register_user, login_user, hash_password, create_token
│   │
│   ├── utils/                    # Helpers: decorators, validators, error handlers
│   │   ├── __init__.py
│   │   ├── decorators.py         # @token_required (JWT check for API)
│   │   ├── validators.py         # validate_email, validate_password, validate_task_data, etc.
│   │   └── error_handlers.py     # Register 400, 401, 404, 422, 500 handlers (JSON)
│   │
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html             # Layout: nav, flash messages, block content
│   │   ├── login.html            # Login form
│   │   ├── register.html         # Register form
│   │   ├── dashboard.html        # Summary and recent tasks
│   │   ├── tasks/                # Task list, form (create/edit), detail
│   │   │   ├── list.html
│   │   │   ├── form.html
│   │   │   └── detail.html
│   │   └── categories/           # Category list, form (create/edit)
│   │       ├── list.html
│   │       └── form.html
│   │
│   └── static/                   # Static assets
│       └── style.css             # CSS for the web UI
│
├── tests/                        # Tests (pytest)
│   ├── __init__.py
│   └── test_auth.py              # Register, login, protected route without token
│
├── config.py                     # Config classes: Development, Testing, Production
├── run.py                        # Entry point: create app, db.create_all(), run server
├── requirements.txt              # Python dependencies
│
├── README.md                     # This file: overview, setup, structure, commands
├── TUTORIAL.md                   # Step-by-step learning flow (Steps 1–13)
├── DEMO_WALKTHROUGH.md           # How to run, test API/UI, common mistakes, debugging
├── INTERVIEW_QUESTIONS.md        # Beginner, intermediate, scenario questions + answers
├── ASSESSMENT.md                 # MCQs, coding assignments, debugging, enhancements
└── PROJECT_README.md              # Shorter reference (overview, setup, testing)
```

### Design Patterns Used

- **Factory pattern:** `create_app(config_name)` creates the app with the right config.
- **Blueprint pattern:** Auth, tasks, categories, and web UI are separate blueprints.
- **Service layer:** Routes call services (e.g. `auth_service.register_user`) for business logic.
- **Separation of concerns:** Routes = HTTP; services = logic; models = data; utils = decorators, validators, errors.
- **Environment-based config:** `config.py` uses `os.environ.get(...)` for secrets and DB URL.

---

## 6. Commands to Run

| Command | Description |
|--------|-------------|
| `python run.py` | Start the Flask development server (http://127.0.0.1:5000) |
| `pip install -r requirements.txt` | Install dependencies |
| `pytest tests/ -v` | Run tests |

Optional (if you use Flask-Migrate later):

```bash
set FLASK_APP=run.py   # Windows
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## 7. Assessment Instructions

Use these documents in order:

1. **TUTORIAL.md**  
   Follow the 13 steps: setup → structure → routing → templates → forms → database → auth → blueprints → CRUD → REST → errors → testing → deployment. Run the app and try each feature.

2. **DEMO_WALKTHROUGH.md**  
   Run the project, test the API with Postman, test the UI in the browser, and read the sections on common mistakes and debugging.

3. **INTERVIEW_QUESTIONS.md**  
   Check your understanding with beginner, intermediate, and scenario-based questions. Use the answers to explain concepts in your own words.

4. **ASSESSMENT.md**  
   Do the MCQs, coding assignments, debugging tasks, and feature enhancements. Use the evaluation criteria to self-check or get feedback from a mentor.

---

## 8. Quick Links

| Document | Purpose |
|----------|---------|
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step learning flow with concepts and code |
| [DEMO_WALKTHROUGH.md](DEMO_WALKTHROUGH.md) | Run, test API/UI, mistakes, debugging |
| [INTERVIEW_QUESTIONS.md](INTERVIEW_QUESTIONS.md) | Interview-style Q&A |
| [ASSESSMENT.md](ASSESSMENT.md) | MCQs, coding, debugging, enhancements |
| [../README.md](../README.md) | Parent training guide (5-day roadmap, project requirements) |

---

## 9. What’s Next

After finishing this project:

- Add more tests (e.g. task CRUD, category CRUD, ownership checks).
- Add search (e.g. by task title) and more filters.
- Use Flask-Migrate for schema changes.
- Move on to **Django REST Framework** or **FastAPI** and compare with this Flask design.

**Good luck.** Focus on understanding concepts; syntax can always be looked up. Build, break, fix, and learn.
