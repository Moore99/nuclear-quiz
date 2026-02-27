
"""
init_db.py
Run once to create the database and seed sample questions.
Usage: python init_db.py
"""

import sqlite3

DATABASE = "nuclear_quiz.db"

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    with open("schema.sql") as f:
        db.executescript(f.read())

    db.commit()
    print("Database initialized and categories seeded.")
    seed_sample_questions(db)
    db.commit()
    print("Sample questions loaded.")
    db.close()

