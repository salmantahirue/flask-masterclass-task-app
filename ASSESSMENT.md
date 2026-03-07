# Flask Task Management System — Assessment for Interns

Use this after completing the tutorial to check understanding and coding skills.

---

## Part 1: Multiple Choice Questions

**1. Which HTTP method should be used to create a new task in a REST API?**  
   (a) GET  
   (b) POST  
   (c) PUT  
   (d) DELETE  
   **Answer: (b) POST.** GET is for reading; PUT is for full update; DELETE is for removal. Creating a resource is POST.

**2. What status code should the server return when a client sends an invalid JWT?**  
   (a) 200  
   (b) 400  
   (c) 401  
   (d) 404  
   **Answer: (c) 401 Unauthorized.** Invalid or missing token means the client is not authenticated.

**3. In SQLAlchemy, a Task has `user_id = db.Column(db.Integer, db.ForeignKey("users.id"))`. This represents:**  
   (a) One task has many users  
   (b) One user has many tasks  
   (c) Many-to-many between users and tasks  
   (d) No relationship  
   **Answer: (b).** The foreign key is on the Task side, so many tasks can point to one user: one user has many tasks.

**4. What is the main purpose of the `create_app()` function?**  
   (a) To run the server  
   (b) To create the Flask app and load config, extensions, and blueprints  
   (c) To define routes  
   (d) To connect to the database only  
   **Answer: (b).** The factory creates the app, applies config, initializes extensions (db, migrate), and registers blueprints.

**5. Why do we store `password_hash` instead of the plain password in the User model?**  
   (a) To save space  
   (b) To allow faster login  
   (c) So that if the database is leaked, the actual passwords cannot be recovered  
   (d) To make the password longer  
   **Answer: (c).** Hashing is one-way; we only verify by comparing the submitted password with the stored hash.

---

## Part 2: Coding Assignments

**Task A: Add a “completed_at” field to Task**  
- Add a nullable `completed_at` (DateTime) column to the Task model.  
- When status is set to `"completed"`, set `completed_at` to the current time.  
- When status is changed from `"completed"` to something else, set `completed_at` back to `None`.  
- Include `completed_at` in the task’s JSON response (`to_dict()`).  
- **Concepts**: Model fields, migration or `db.create_all()`, request body handling, JSON serialization.

**Task B: Add a simple search endpoint**  
- Add optional query parameter `q` to `GET /api/tasks`.  
- If `q` is present, filter tasks where the title contains `q` (case-insensitive).  
- Still apply `user_id` and existing filters (status, priority, category_id).  
- **Concepts**: Query parameters, filtering, SQLAlchemy `.filter()`, `.ilike()`.

**Task C: Return 404 when category not found**  
- In `GET /api/categories/<id>`, if the category does not exist or does not belong to the current user, return JSON `{"error": "Category not found"}` with status 404.  
- **Concepts**: Ownership check, consistent error format, status codes.

---

## Part 3: Debugging Tasks

**Scenario 1:** A colleague says “When I POST to /api/auth/register with a valid email and password, I get 500.”  
- **What could cause this?** Possible causes: database not created (`db.create_all()` not run), missing or wrong `SECRET_KEY`, typo in model or column name, unique constraint (e.g. email already exists) not handled.  
- **What would you check?** Server logs/stack trace, database file exists, request body (content-type JSON, correct keys), and whether the email is already in the database.

**Scenario 2:** “GET /api/tasks returns all tasks from all users.”  
- **What is wrong?** The list endpoint is not filtering by `current_user.id`.  
- **Fix:** Use `Task.query.filter_by(user_id=current_user.id)` (and keep other filters). Ensure the route is protected with `@token_required` and that `current_user` is set from the JWT.

**Scenario 3:** “After login, the web UI dashboard still redirects me to login.”  
- **What could cause this?** Session not being set (e.g. `session["user_id"] = user.id` missing after login), or `SECRET_KEY` not set (so session cookie is invalid).  
- **Fix:** Ensure the login route sets `session["user_id"]` and that the app has a non-empty `SECRET_KEY` in config.

---

## Part 4: Feature Enhancement Tasks

**Enhancement 1: Pagination for categories**  
- Add optional `page` and `per_page` to `GET /api/categories`.  
- Return a structure like `{"categories": [...], "total": N, "page": 1, "per_page": 10}`.  
- **Concepts:** Query parameters, `.paginate()`, consistent API shape.

**Enhancement 2: Change password (API)**  
- Implement `PUT /api/auth/change-password` (or ensure it exists).  
- Body: `{"current_password": "...", "new_password": "..."}`.  
- Check current password, validate new password length, hash and save. Return 200 or 400/401 with a clear message.  
- **Concepts:** Validation, password hashing, ownership (only the logged-in user).

**Enhancement 3: Task detail in web UI**  
- Ensure the task detail page shows title, description, status, priority, due date, category.  
- Add an “Edit” link to the edit form and a “Delete” button that asks for confirmation.  
- **Concepts:** Jinja2 templates, links, forms, confirmation, redirects.

---

## Evaluation Criteria

- **Correctness:** Does the code do what the requirement asks? (status codes, filters, ownership.)  
- **Security:** No plain-text passwords; JWT/session used correctly; user can only access own data.  
- **Consistency:** Same JSON shape and error format as the rest of the API.  
- **Code quality:** Readable names, no duplicated logic where a service or decorator could be used.  
- **Understanding:** Can the intern explain why they used a given status code, filter, or pattern?

Use these exercises for self-assessment or for mentor-led evaluation after the Flask training.
