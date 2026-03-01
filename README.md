# Task Manager API (Flask)

REST API for task management built with Flask, SQLAlchemy and JWT authentication.
This project was designed as a production-style backend with pagination, filtering, rate limiting, admin routes, soft delete and automatic Swagger documentation.

---

## Features

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

---

## Tech stack

* Python 3.11+
* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-Migrate
* Flask-Limiter
* Flasgger (Swagger UI)
* Redis
* Docker
* SQLite / PostgreSQL compatible

---

## Project structure

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

migrations/

tests/

docker-compose.yml
requirements.txt
run.py
.env.example
README.md
```

---

## Installation

Clone repository

```
git clone https://github.com/your-user/task-manager-flask.git
cd task-manager-flask
```

Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

## Environment variables

Create `.env`

```
SECRET_KEY=dev-secret
JWT_SECRET_KEY=jwt-secret
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
```

---

## Running locally

```
flask db upgrade
flask run
```

API will run at:

```
http://localhost:5000
```

Swagger docs:

```
http://localhost:5000/apidocs
```

---

## Running with Docker

```
docker-compose up --build
```

---

## Authentication

Login:

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

Use token:

```
Authorization: Bearer <token>
```

---

## Tasks endpoints

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

## Admin endpoints

```
GET /api/v1/admin/tasks
GET /api/v1/admin/users
GET /api/v1/admin/events
```

Admin token required.

---

## Pagination format

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

## Filters

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

## Rate limiting

Configured with Flask-Limiter + Redis.

Example:

* login → 5/min
* signup → 2/min
* tasks → 120/min

---

## Migrations

```
flask db migrate
flask db upgrade
```

---

## License

MIT
