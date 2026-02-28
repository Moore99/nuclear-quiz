#!/usr/bin/env python3
"""
Script to reset the admin password to a known working value.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")

def reset_admin_password():
    """Reset the admin password to 'admin123' using the current werkzeug version."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    username = "johnhmoore01@gmail.com"
    new_password = "admin123"
    new_hash = generate_password_hash(new_password)
    
    c.execute("UPDATE users SET hash = ? WHERE username = ?", (new_hash, username))
    conn.commit()
    
    print(f"Admin password reset for {username}")
    print(f"New password: {new_password}")
    print(f"New hash: {new_hash}")
    print("Please try logging in with this password.")
    
    conn.close()

if __name__ == "__main__":
    reset_admin_password()