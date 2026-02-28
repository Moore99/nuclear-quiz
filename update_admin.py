import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

# add is_admin column if it doesn't exist
try:
    c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    print("Added is_admin column")
except sqlite3.OperationalError as e:
    print("Column already exists or error", e)

# update user
newhash = generate_password_hash('test123')
c.execute("UPDATE users SET hash = ?, is_admin = 1 WHERE username = ?", (newhash, 'johnhmoore01@gmail.com'))
conn.commit()
print('rows affected', c.rowcount)
# report user
c.execute("SELECT id, username, is_admin FROM users WHERE username = ?", ('johnhmoore01@gmail.com',))
print(c.fetchall())
conn.close()
