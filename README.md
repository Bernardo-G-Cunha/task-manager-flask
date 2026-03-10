# Task Manager API (Flask)

REST API for task management built with Flask, SQLAlchemy and JWT authentication.
This project was designed as a **production-style backend** with pagination, filtering, rate limiting, admin routes, soft delete, automated tests with pytest and automatic Swagger documentation.

**Live API**

```
https://task-manager-flask-vcwa.onrender.com
```

Swagger documentation:

```
https://task-manager-flask-vcwa.onrender.com/apidocs
```

---

# Features

* JWT authentication
* Task CRUD
* Tags support
* Pagination
* Filtering
* Soft delete
* Admin endpoints
* Rate limiting (Redis)
* Swagger documentation (Flasgger)
* Docker support
* Database migrations (Flask-Migrate)
* PostgreSQL production database

---

# Tech stack

* Python 3.11+
* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-Migrate
* Flask-Limiter
* Flasgger (Swagger UI)
* Redis
* PostgreSQL
* Docker
* SQLite (local development)
* Pytest (testing)

---

# Project structure

```
app/
    __init__.py
    auth/
    dtos/
    exceptions/
    models/
    routes/
    schemas/
    services/
    extensions.py
    config.py

migrations/
tests/

docker-compose.yml
Dockerfile
entrypoint.sh
init-db.sql
pyproject.toml
requirements.txt
requirements-dev.txt
run.py
.env.example
README.md
```

---

# Installation

Clone repository

```
git clone https://github.com/your-user/task-manager-flask.git
cd task-manager-flask
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Linux / Mac:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
pip install -e .
```

---

# Environment variables

Copy the example file

```
cp .env.example .env
```

Edit environment variables according to your environment.

---

# Running locally

Run migrations:

```
flask db upgrade
```

Start server:

```
flask run
```

API:

```
http://localhost:5000
```

Swagger docs:

```
http://localhost:5000/apidocs
```

---

# Running with Docker

Build and start containers:

```
docker-compose up --build
```

This will start:

* Flask API
* PostgreSQL
* Redis

---

# Deployment

The API is deployed on **Render** using Docker containers.

Production services:

* **Web service:** Flask API container
* **Database:** PostgreSQL
* **Cache / rate limiting:** Redis

Environment variables are configured through the Render dashboard.

---

# Authentication

Login endpoint:

```
POST /api/v1/auth
```

Response:

```
{
  "success": true,
  "data": {
    "access_token": "..."
  }
}
```

Authenticated requests must include:

```
Authorization: Bearer <token>
```

---

# Tasks endpoints

```
GET    /api/v1/tasks
POST   /api/v1/tasks
GET    /api/v1/tasks/<id>
PATCH  /api/v1/tasks/<id>
DELETE /api/v1/tasks/<id>
```

Supports:

* pagination
* sorting
* filters
* date range

Example:

```
/api/v1/tasks?page=1&limit=10&sort=created_at&order=desc
```

---

# Admin endpoints

```
GET /api/v1/admin/tasks
GET /api/v1/admin/users
GET /api/v1/admin/events
```

Admin token required.

---

# Pagination format

```
{
  "success": true,
  "data": {
    "tasks": []
  },
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

---

# Filters

Supported filters:

* id
* name
* done
* created_from
* created_to

Example:

```
/api/v1/admin/tasks?done=true&created_from=2024-01-01
```

---

# Rate limiting

Implemented using **Flask-Limiter + Redis**.

Examples:

* login → 5/min
* signup → 2/min
* tasks → 120/min

---

# Database migrations

Create migration:

```
flask db migrate
```

Apply migration:

```
flask db upgrade
```

---

# License

MIT
