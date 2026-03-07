# Demo Project Walkthrough

This guide shows you how to run the Task Management System, test the API and UI, avoid common mistakes, and debug effectively. Use it during or after the tutorial.

---

## 1. How to Run the Project

### Step 1: Open the project folder

```bash
cd task_management_system
```

Make sure you are inside the folder that contains `run.py`, `config.py`, and the `app` folder.

### Step 2: Create and activate a virtual environment

**Windows (PowerShell or CMD):**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the server

```bash
python run.py
```

You should see something like:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The first run creates the SQLite database file (e.g. `task_management.db`) and all tables. Leave the server running while you test.

### Step 5: Open the app in a browser

Open **http://127.0.0.1:5000**. You should be redirected to the **Login** page.

---

## 2. How to Test the API

Use **Postman**, **Insomnia**, or **curl**. The API uses JSON and JWT for protected routes.

### 2.1 Register a user

- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/api/auth/register`  
- **Headers:** `Content-Type: application/json`  
- **Body (raw JSON):**

```json
{
  "email": "intern@company.com",
  "password": "secret123",
  "username": "Intern One"
}
```

**Expected:** Status **201**, body with `user` (id, email, username) and `token`. Copy the `token` for the next steps.

### 2.2 Login (get a new token)

- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/api/auth/login`  
- **Headers:** `Content-Type: application/json`  
- **Body:**

```json
{
  "email": "intern@company.com",
  "password": "secret123"
}
```

**Expected:** Status **200**, body with `user` and `token`. Copy the `token`.

### 2.3 Call protected endpoints

For every request below, add this header:

- **Header:** `Authorization: Bearer <paste-your-token-here>`

**Get my profile**

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/auth/profile`  
- **Expected:** 200, your user object.

**Create a task**

- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/api/tasks`  
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer <token>`  
- **Body:**

```json
{
  "title": "Learn Flask routing",
  "description": "Complete Step 3 of the tutorial",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-02-01T18:00:00"
}
```

**Expected:** 201, task object with `id`.

**List my tasks**

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/tasks`  
- **Optional query:** `?status=pending&priority=high&page=1&per_page=10`  
- **Expected:** 200, `{"tasks": [...], "total": N, "page": 1, "per_page": 10}`.

**Get one task**

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/tasks/1`  
- **Expected:** 200, task object; or 404 if not found or not yours.

**Update a task**

- **Method:** PUT  
- **URL:** `http://127.0.0.1:5000/api/tasks/1`  
- **Body:** Same shape as create (title, description, status, priority, due_date, category_id).  
- **Expected:** 200, updated task.

**Delete a task**

- **Method:** DELETE  
- **URL:** `http://127.0.0.1:5000/api/tasks/1`  
- **Expected:** 200, `{"message": "Task deleted"}`.

**Create a category**

- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/api/categories`  
- **Body:** `{"name": "Work"}`  
- **Expected:** 201, category object.

**List my categories**

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/categories`  
- **Expected:** 200, `{"categories": [...]}`.

**Get tasks in a category**

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/categories/1/tasks`  
- **Expected:** 200, `{"tasks": [...]}`.

### 2.4 Test errors (no token / wrong token)

- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/api/auth/profile`  
- **Headers:** Do **not** send `Authorization`.  
- **Expected:** 401, `{"error": "Token is missing"}`.

---

## 3. How to Test the UI

1. Open **http://127.0.0.1:5000**. You are redirected to **Login**.
2. Click **Register**. Fill email, password, optional username. Submit. You should be logged in and see the **Dashboard**.
3. **Dashboard:** Summary (pending/completed counts) and recent tasks. Use “View all tasks” or the **Tasks** link in the nav.
4. **Tasks:** List of your tasks. Use “New Task” to create one. Fill title, description, status, priority, due date, category. Save. Click a task to see **Task detail**. Use Edit and Delete.
5. **Categories:** List of your categories. Create and edit categories. From the task list you can filter by category (query param or link).
6. **Logout:** Click Logout. You are redirected to Login. Visiting Dashboard or Tasks without logging in redirects you to Login.

---

## 4. Common Intern Mistakes

| Mistake | Why it happens | Fix |
|--------|----------------|-----|
| **401 on every API call** | Forgot `Authorization: Bearer <token>` | Add the header to every request to `/api/auth/*`, `/api/tasks`, `/api/categories`. |
| **Seeing another user’s tasks** | Not filtering by `user_id` | Always use `Task.query.filter_by(user_id=current_user.id)` (and same for categories). |
| **Plain-text passwords in DB** | Storing `password` instead of hashing | Use bcrypt (or similar) and store only `password_hash`. |
| **500 or HTML error for API** | No error handler or wrong content type | Use `@app.errorhandler(404)` etc. and return `jsonify({"error": "..."})` with the right status. |
| **Secrets in code** | Hardcoding `SECRET_KEY` or DB URL | Use `.env` and `os.environ.get(...)` in config. |
| **Wrong Content-Type** | Sending JSON without header | Set `Content-Type: application/json` for POST/PUT with a JSON body. |
| **Token in URL** | Putting token in query string | Put token only in the `Authorization: Bearer <token>` header. |

---

## 5. Debugging & Best Practices

### Read the console

Flask prints tracebacks in the terminal. Read the last few lines to see the error and the file/line number.

### Inspect request data

In a route or service, temporarily add:

```python
print("request.json:", request.get_json())
print("current_user:", current_user)
```

Remove or comment out before committing.

### Use the debugger

In your IDE, set a breakpoint in a route (e.g. inside `create_task`). Run the app in debug mode (`python run.py` with `debug=True`). When the request hits the breakpoint, inspect variables.

### Check the database

- SQLite file is created in the project root (e.g. `task_management.db`). Use a SQLite browser or `sqlite3` to run `SELECT * FROM users;` or `SELECT * FROM tasks;` and confirm data.
- If tables are missing, ensure `db.create_all()` runs (e.g. in `run.py` inside `with app.app_context():`).

### API checklist

- URL correct (e.g. `/api/tasks` not `/api/task`).
- HTTP method correct (POST for create, GET for list, etc.).
- Headers: `Content-Type: application/json` for body; `Authorization: Bearer <token>` for protected routes.
- Body: valid JSON; required fields (e.g. `title` for task) present.

### Best practices

- **One feature at a time:** Get register → login → create task working before adding filters or categories.
- **Test with Postman first:** Easier to see status code and body than only from the browser.
- **Keep tokens safe:** Don’t commit `.env` or paste real tokens into docs; use a test user and token for demos.
- **Consistent errors:** Always return `{"error": "..."}` (or similar) and the right status code (400, 401, 404) so the client can handle them.

---

## 6. Quick Reference: Main URLs

| What | URL |
|------|-----|
| Web: Login | http://127.0.0.1:5000/login |
| Web: Register | http://127.0.0.1:5000/register |
| Web: Dashboard | http://127.0.0.1:5000/dashboard |
| Web: Tasks | http://127.0.0.1:5000/tasks |
| Web: Categories | http://127.0.0.1:5000/categories |
| API: Register | POST /api/auth/register |
| API: Login | POST /api/auth/login |
| API: Profile | GET /api/auth/profile |
| API: Tasks | GET/POST /api/tasks, GET/PUT/DELETE /api/tasks/<id> |
| API: Categories | GET/POST /api/categories, GET/PUT/DELETE /api/categories/<id>, GET /api/categories/<id>/tasks |

Use this walkthrough next to the **TUTORIAL.md** and **README.md** while you run and test the Task Management System.
