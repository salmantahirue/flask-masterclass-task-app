# Flask Backend Development Training Guide

## Welcome!

Welcome to your Flask backend development training! This guide will help you understand what you'll learn, why we're starting with Flask, and how to approach your learning journey.

---

## Why Flask First?

Flask is a **minimalist** web framework for Python. We're starting with Flask because:

1. **Simplicity**: Flask has a small core and minimal abstractions, making it easier to understand how web APIs work at a fundamental level
2. **Explicit is Better Than Implicit**: Flask doesn't hide complexity—you'll see exactly what's happening, which builds a strong foundation
3. **Foundation for Other Frameworks**: Understanding Flask makes Django REST Framework and FastAPI easier to learn later
4. **Industry Standard**: Flask is widely used in production, so these skills are immediately applicable

---

## Learning Roadmap & Expectations

### Timeline
- **Duration**: 5 days
- **Time Commitment**: 6-8 hours per day
- **Approach**: Project-based learning with hands-on practice

### Learning Phases

#### Day 1: Flask Basics & HTTP Fundamentals
- Understanding HTTP protocol and how web APIs work
- Flask installation and setup
- Routes, request/response cycle
- Building simple API endpoints
- JSON data handling

#### Day 2: REST API Design & Database Integration
- REST API design principles
- SQLAlchemy ORM basics
- Database models and relationships
- CRUD operations with Flask

#### Day 3: Authentication & Security
- JWT (JSON Web Tokens) authentication
- Password hashing
- Protected routes
- Input validation

#### Day 4-5: Project Development
- Building Task Management API
- Code organization and best practices
- Error handling
- Testing API endpoints

### Expectations

**What We Expect:**
- ✅ Focus on **understanding concepts**, not memorizing syntax
- ✅ Ask questions when something is unclear
- ✅ Build the project to reinforce learning
- ✅ Write clean, readable code

**What We Don't Expect:**
- ❌ Perfect code on the first try
- ❌ Memorizing every Flask function

**Remember**: The goal is to build a strong foundation. Syntax can be looked up, but concepts must be understood.

---

## Important Topics to Focus On

### 1. HTTP & API Fundamentals

**Key Concepts:**
- Client-Server architecture
- Request-Response cycle
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- HTTP status codes: 200, 201, 400, 401, 404, 500
- JSON data format
- Stateless communication

---

### 2. REST API Concepts

**REST Principles:**
- Resources identified by URLs (`/api/users/123`)
- Use HTTP methods for operations (GET, POST, PUT, DELETE)
- Use nouns for resources, not verbs (`/api/users` not `/api/getUsers`)
- Use plural nouns (`/api/users` not `/api/user`)
- Stateless requests

---

### 3. Flask Core Concepts

**Essential Flask Components:**

1. **Application Instance** - The Flask app object
2. **Routes** - `@app.route()` decorator maps URLs to functions
3. **Request Object** - Access incoming data (JSON, headers)
4. **Response Object** - Return JSON with status codes
5. **Blueprint** - Organize routes into modules
6. **Error Handling** - Custom error handlers

---

### 4. Database & SQLAlchemy

**Key Concepts:**
- **Models**: Python classes representing database tables
- **ORM**: Use Python code instead of raw SQL
- **Relationships**: One-to-many, many-to-many
- **Queries**: Filtering, sorting, querying data
- **Migrations**: Database schema changes

---

### 5. Authentication & Security

**JWT Authentication:**
- Token-based authentication
- Token structure: Header.Payload.Signature
- Token expiration

**Security Basics:**
- Hash passwords (never store plain text)
- Validate all input
- Protect routes with decorators

---

## Project Requirements: Task Management API

### Project Overview

Build a RESTful API for a task management system. Users can register, login, create tasks, and organize them into categories.

### What You Need to Build

**User Features:**
- Register with email and password
- Login and get authentication token
- View and update profile

**Task Features:**
- Create, read, update, and delete tasks
- Each task has: title, description, status (pending/in-progress/completed), priority (low/medium/high), due date
- Filter tasks by status, priority, or due date
- Users can only see their own tasks

**Category Features:**
- Create categories (e.g., "Work", "Personal")
- Assign tasks to categories
- View all tasks in a category
- Users can only see their own categories

### API Endpoints

**Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (protected)
- `PUT /api/auth/profile` - Update profile (protected)

**Tasks:**
- `POST /api/tasks` - Create task (protected)
- `GET /api/tasks` - Get all tasks with filters (protected)
- `GET /api/tasks/<id>` - Get single task (protected)
- `PUT /api/tasks/<id>` - Update task (protected)
- `DELETE /api/tasks/<id>` - Delete task (protected)

**Categories:**
- `POST /api/categories` - Create category (protected)
- `GET /api/categories` - Get all categories (protected)
- `GET /api/categories/<id>` - Get single category (protected)
- `PUT /api/categories/<id>` - Update category (protected)
- `DELETE /api/categories/<id>` - Delete category (protected)
- `GET /api/categories/<id>/tasks` - Get tasks in category (protected)

### Database Models

**User:**
- id, email (unique), password_hash, username, created_at, updated_at

**Task:**
- id, title, description, status, priority, due_date, user_id, category_id, created_at, updated_at

**Category:**
- id, name, user_id, created_at, updated_at

**Relationships:**
- User has many Tasks
- User has many Categories
- Category has many Tasks
- Task belongs to one User
- Task belongs to one Category (optional)

### Project Structure

```
task_management_api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   ├── routes/              # API routes
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── categories.py
│   └── utils/               # Helpers
│       ├── validators.py
│       └── decorators.py    # Auth decorator
├── migrations/              # Database migrations
├── requirements.txt
└── run.py                   # Entry point
```

### Skills This Project Covers

- ✅ Flask routes and HTTP methods
- ✅ RESTful API design
- ✅ SQLAlchemy models and relationships
- ✅ JWT authentication
- ✅ Password hashing
- ✅ Protected routes
- ✅ Error handling
- ✅ Input validation
- ✅ Code organization

---

## Getting Started

### Prerequisites

- [ ] Python 3.8+ installed
- [ ] Basic Python OOP knowledge
- [ ] Command line familiarity
- [ ] Code editor (VS Code recommended)

### Setup Steps

1. Create virtual environment
2. Install Flask, SQLAlchemy, Flask-Migrate, PyJWT, bcrypt
3. Set up project structure
4. Start with authentication endpoints
5. Add task CRUD operations
6. Implement categories
7. Add filtering and error handling

---

## Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT Introduction](https://jwt.io/introduction)

**Tools:**
- Postman/Insomnia - Test API endpoints
- SQLite - Start with SQLite database
- Flask-Migrate - Database migrations

---

## Common Pitfalls to Avoid

1. **Don't Skip Fundamentals**: Understanding HTTP and REST is crucial
2. **Don't Memorize Syntax**: Focus on concepts
3. **Don't Ignore Error Handling**: Handle errors gracefully
4. **Don't Hardcode Values**: Use environment variables
5. **Don't Ignore Security**: Always hash passwords, validate input

---

## Assessment Criteria

Your project will be evaluated on:

- ✅ **Functionality**: All endpoints working correctly
- ✅ **Code Quality**: Clean, readable, organized code
- ✅ **API Design**: RESTful, proper HTTP methods and status codes
- ✅ **Security**: Authentication, password hashing, input validation
- ✅ **Error Handling**: Meaningful error messages

---

## Support & Questions

- **Ask questions early** - Don't struggle in silence
- **Read error messages** - They usually tell you what's wrong
- **Use debugging tools** - Print statements, debugger
- **Review your code** - Step back and read it fresh

---

## What's Next?

After completing this Flask training:
1. You'll move to **Django REST Framework**
2. Then **FastAPI**
3. Each framework builds on your Flask foundation

**Good luck! Remember: focus on understanding, not memorizing. Build, break, fix, and learn!** 🚀
