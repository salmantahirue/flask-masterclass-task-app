# Flask Task Management System — Interview Questions

Questions are grouped by level. Use them to check understanding after the tutorial.

---

## Beginner Flask Questions

**1. What is Flask?**  
Flask is a lightweight web framework for Python. It gives you routing (URL → function), request/response handling, and extensions for databases and auth. You build the structure yourself, which helps you learn how web apps work.

**2. What is a route?**  
A route maps a URL (and HTTP method) to a Python function. When a client requests that URL, Flask runs the function and returns its response (e.g. JSON or HTML).

**3. What is a Blueprint?**  
A Blueprint is a set of routes (and optional templates/static) that you register on the app. It keeps code organized by feature (e.g. auth, tasks, categories) instead of putting everything in one file.

**4. What is the difference between GET and POST?**  
GET is for reading data; it should not change server state. POST is for creating or submitting data (e.g. register, create task). In this project, GET is used to list tasks; POST is used to create a task.

**5. What is the request object?**  
The Flask `request` object holds the current HTTP request: URL, method, headers, and body (e.g. `request.get_json()` for JSON, `request.args` for query parameters).

**6. How do you return JSON from a Flask route?**  
Use `from flask import jsonify` and return `jsonify({"key": "value"})`. You can add a status code: `jsonify({"error": "Not found"}), 404`.

**7. What is the Factory Pattern in Flask?**  
The factory is a function (e.g. `create_app(config_name)`) that creates and configures the Flask app. It lets you use different configs for development, testing, and production with the same codebase.

**8. What is Jinja2?**  
Jinja2 is Flask’s template engine. You write HTML with placeholders (`{{ variable }}`) and blocks (`{% block content %}`) so the server can inject data and reuse layout (e.g. `base.html`).

---

## Intermediate Flask Questions

**9. What is SQLAlchemy ORM?**  
ORM (Object-Relational Mapping) lets you work with the database using Python classes (models) instead of raw SQL. You define models (e.g. `Task`), relationships (e.g. user has many tasks), and use sessions to add, query, and commit.

**10. What is a one-to-many relationship?**  
One record in table A can be linked to many records in table B. Example: one User has many Tasks. In the database, the Task table has a `user_id` foreign key pointing to User.

**11. What is JWT and why use it for APIs?**  
JWT (JSON Web Token) is a signed token that encodes user identity (e.g. `user_id`). The client sends it in the `Authorization: Bearer <token>` header. The server verifies the signature and reads the user id. It’s stateless and works well for REST APIs.

**12. What is the purpose of a decorator like `@token_required`?**  
The decorator runs before the route. It reads the JWT from the request, verifies it, loads the user, and passes `current_user` into the route. If the token is missing or invalid, it returns 401 without running the route. So protected routes don’t repeat the same auth logic.

**13. Why hash passwords instead of storing them in plain text?**  
If the database is leaked, plain-text passwords are exposed. A hash is one-way: you can check a password against the hash, but you can’t recover the password from the hash. We use bcrypt to hash passwords before saving.

**14. What is the difference between authentication and authorization?**  
Authentication = “Who are you?” (login, verify identity). Authorization = “What are you allowed to do?” (e.g. only your own tasks). In this project, JWT/session handles authentication; checking `task.user_id == current_user.id` handles authorization.

**15. Why use a service layer (e.g. `auth_service.register_user`)?**  
Routes should handle HTTP (parse request, return response). Business logic (e.g. “check email exists”, “hash password”, “create user”) lives in services. That way the same logic can be used from API routes, web routes, or tests without duplicating code.

**16. What are Flask error handlers?**  
They are functions registered with `@app.errorhandler(404)` (or 400, 401, 500). When an exception or abort happens, Flask calls the right handler so you return a consistent JSON (or HTML) instead of a default error page.

---

## Scenario-Based Questions

**17. A client sends POST /api/tasks without a token. What should happen?**  
The `@token_required` decorator runs first. It finds no (or invalid) token and returns 401 Unauthorized with a message like "Token is missing" or "Invalid token". The route body is never executed.

**18. A client sends GET /api/tasks/999 but the task belongs to another user. What should happen?**  
The route loads the task with `Task.query.filter_by(id=999, user_id=current_user.id).first()`. If no row is found, the task either doesn’t exist or isn’t owned by the current user. The route returns 404 "Task not found" so we don’t leak whether the task exists.

**19. How would you add “search tasks by title”?**  
In the list-tasks route, read a query parameter (e.g. `q = request.args.get("q")`). If present, add a filter: `Task.title.ilike(f"%{q}%")` (with sanitization/parameterization to avoid SQL injection). Return the same paginated list format.

**20. Why might we use Flask-Migrate instead of only `db.create_all()`?**  
`db.create_all()` creates tables that don’t exist but does not change existing tables. When you add or change columns (e.g. add a “tags” column to Task), you need migrations to alter the schema safely. Flask-Migrate generates migration scripts and applies them so the database stays in sync with the models.

---

## Summary

- **Beginner**: Routes, Blueprints, GET/POST, request, jsonify, factory, Jinja2.  
- **Intermediate**: ORM, relationships, JWT, decorators, password hashing, auth vs authorization, service layer, error handlers.  
- **Scenario**: Token required, ownership checks, search, migrations.

Use these answers as a reference; try to explain them in your own words when practicing.
