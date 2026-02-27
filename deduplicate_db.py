"""
deduplicate_db.py
Removes duplicate categories and questions from nuclear_quiz.db.
Safe to run multiple times (idempotent).
"""
import sqlite3
import os

DATABASE = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")
)

def report(db, label):
    cats = db.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    qs = db.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    ans = db.execute("SELECT COUNT(*) FROM answers").fetchone()[0]
    print(f"{label}: {cats} categories, {qs} questions, {ans} answers")

def deduplicate(db):
    # ── 1. Duplicate categories ───────────────────────────────────────────
    # For each name, keep the lowest category id, delete the rest.
    dup_cats = db.execute("""
        SELECT id, name FROM categories
        WHERE id NOT IN (
            SELECT MIN(id) FROM categories GROUP BY LOWER(name)
        )
        ORDER BY id
    """).fetchall()

    if dup_cats:
        print(f"\nDuplicate categories to remove ({len(dup_cats)}):")
        for cat in dup_cats:
            canonical_id = db.execute(
                "SELECT MIN(id) FROM categories WHERE LOWER(name) = LOWER(?)",
                (cat[1],)
            ).fetchone()[0]
            print(f"  cat {cat[0]} '{cat[1]}' → kept as cat {canonical_id}")

            # Reassign questions from duplicate category to canonical category,
            # but only if an identical question doesn't already exist there.
            orphan_qs = db.execute(
                "SELECT id FROM questions WHERE category_id = ?", (cat[0],)
            ).fetchall()

            for (qid,) in orphan_qs:
                q_text = db.execute(
                    "SELECT question_text FROM questions WHERE id = ?", (qid,)
                ).fetchone()[0]
                already_exists = db.execute("""
                    SELECT id FROM questions
                    WHERE category_id = ? AND LOWER(question_text) = LOWER(?)
                """, (canonical_id, q_text)).fetchone()

                if already_exists:
                    # True duplicate — delete answers then question
                    db.execute("DELETE FROM answers WHERE question_id = ?", (qid,))
                    db.execute("DELETE FROM questions WHERE id = ?", (qid,))
                else:
                    # Different question that ended up in wrong category — keep it
                    db.execute(
                        "UPDATE questions SET category_id = ? WHERE id = ?",
                        (canonical_id, qid)
                    )

            db.execute("DELETE FROM categories WHERE id = ?", (cat[0],))
    else:
        print("\nNo duplicate categories found.")

    db.commit()

    # ── 2. Duplicate questions within the same category ───────────────────
    # Keep lowest id, delete the rest.
    dup_qs = db.execute("""
        SELECT id FROM questions
        WHERE id NOT IN (
            SELECT MIN(id) FROM questions GROUP BY category_id, LOWER(question_text)
        )
    """).fetchall()

    if dup_qs:
        print(f"\nDuplicate questions to remove: {len(dup_qs)}")
        for (qid,) in dup_qs:
            db.execute("DELETE FROM answers WHERE question_id = ?", (qid,))
            db.execute("DELETE FROM questions WHERE id = ?", (qid,))
    else:
        print("No duplicate questions found.")

    db.commit()

    # ── 3. Orphaned answers (safety check) ───────────────────────────────
    orphans = db.execute("""
        SELECT COUNT(*) FROM answers
        WHERE question_id NOT IN (SELECT id FROM questions)
    """).fetchone()[0]
    if orphans:
        print(f"\nRemoving {orphans} orphaned answers...")
        db.execute("DELETE FROM answers WHERE question_id NOT IN (SELECT id FROM questions)")
        db.commit()


def main():
    print(f"Database: {DATABASE}")
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = OFF")  # allow deletions without cascade issues

    report(db, "Before")
    deduplicate(db)
    report(db, "After")

    print("\nCategories after cleanup:")
    for row in db.execute("SELECT id, name, COUNT(q.id) as n FROM categories c LEFT JOIN questions q ON q.category_id = c.id GROUP BY c.id ORDER BY c.id").fetchall():
        print(f"  {row[0]:2d}. {row[1]} ({row[2]} questions)")

    db.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
