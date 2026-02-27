import os
import sqlite3
from functools import wraps
import jwt
from flask import redirect, request, session, jsonify, g, current_app

import os
DATABASE = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")
)

def get_db():
    """Open a database connection, reuse within a request context."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # lets you access columns by name
    db.execute("PRAGMA foreign_keys = ON")
    return db


def login_required(f):
    """Redirect to login if user is not logged in. Same pattern as CS50 Finance."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Redirect to admin login if not authenticated as admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function


def jwt_required(f):
    """Check Bearer token and set g.user_id. Returns 401 JSON on failure."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            g.user_id = int(payload["sub"])  # sub is stored as str; cast back to int for DB comparisons
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function


def ensure_quiz_sessions_table(db):
    """Create quiz_sessions table if it does not exist. Safe to call on every startup."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            category_id INTEGER NOT NULL REFERENCES categories(id),
            question_ids TEXT NOT NULL,
            current_index INTEGER NOT NULL DEFAULT 0,
            score INTEGER NOT NULL DEFAULT 0,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
