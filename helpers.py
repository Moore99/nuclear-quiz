import os
import sqlite3
from functools import wraps
from flask import redirect, session, g
from flask import current_app

import os
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")

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
