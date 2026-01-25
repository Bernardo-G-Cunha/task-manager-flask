# 📝 Task Manager

A simple task manager web application built with Flask and SQLite.  
**⚠️ This project is currently under development.**

## 🚀 Features

- ✅ Add tasks
- 📋 View task list
- ✏️ Edit tasks
- ❌ Delete tasks
- 📌 Mark tasks as completed
- 🗂 Organized backend structure (routes, models, services, schemas, etc.)

## 🛠️ Technologies Used

- Python 3.x
- Flask
- SQLite
- SQLAlchemy + Flask-Migrate

---

## 📦 How to Run Locally

### 1. Clone this repository

```bash
git clone https://github.com/Bernardo-G-Cunha/task-manager-flask.git
cd task-manager-flask
````

### 2. Create and activate a virtual environment

It’s recommended to use a virtual environment to isolate dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

In the root directory, create a `.env` file with the following content:

```
FLASK_APP=backend/run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///db.sqlite3
```

> Make sure this file exists before running database migrations or starting the app.

### 5. Initialize the database

```bash
flask db init          # Only needed once
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the app

```bash
flask run
```

### 7. Open in your browser

```
http://localhost:5000
```

---

## 🗂 Project Structure

```

task-manager-flask/
│
├── backend/
│   ├── app/
│   │   ├── exceptions/        # Custom exception handlers
│   │   ├── models/            # Database models
│   │   ├── routes/            # Route definitions
│   │   ├── schemas/           # Marshmallow schemas
│   │   ├── services/          # Business logic and helpers
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   └── extensions.py      # Flask extensions setup
│   ├── tests/                 # Unit and integration tests
│   └── run.py                 # Entry point to run the Flask app
│
├── frontend/
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   └── templates/             # HTML templates
│
├── .gitignore
├── requirements.txt           # Python dependencies
├── LICENSE
└── README.md

```
---

## 🌐 Deployment (Coming Soon)

This project is currently under development and can only be run locally.

Soon, it will be deployed to a public URL so anyone can access it as a regular web application.  
Deployment will likely be done using platforms such as **Render**, **Railway**, or **Heroku**.

Once deployed, the link will be added here.

---

## 📌 Notes

* This project is for learning and educational purposes.
* More features will be added soon, such as user authentication and task deadlines.

