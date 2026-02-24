import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, admin_required, get_db

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (same as CS50 Finance)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flask_session")
os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
Session(app)

print("APP STARTED OK")  # add this line

# Admin password (env variable in production, hardcoded for dev)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Must provide username", "danger")
            return render_template("register.html")
        if not password:
            flash("Must provide password", "danger")
            return render_template("register.html")
        if password != confirmation:
            flash("Passwords do not match", "danger")
            return render_template("register.html")

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            flash("Username already taken", "danger")
            return render_template("register.html")

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        db.commit()

        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = user["id"]
        flash("Registered successfully!", "success")
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Must provide username and password", "danger")
            return render_template("login.html")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            flash("Invalid username or password", "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ─────────────────────────────────────────────
# MAIN ROUTES
# ─────────────────────────────────────────────
@app.route("/")
@login_required
def index():
    db = get_db()
    categories = db.execute("""
        SELECT c.id, c.name, c.description, c.icon,
               COUNT(q.id) as question_count
        FROM categories c
        LEFT JOIN questions q ON q.category_id = c.id
        GROUP BY c.id
        ORDER BY c.name
    """).fetchall()
    categories = [dict(c) for c in categories]
    return render_template("index.html", categories=categories)
    

@app.route("/quiz/<int:category_id>")
@login_required
def quiz_start(category_id):
    """Start a new quiz session for a given category."""
    db = get_db()
    category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
    if not category:
        flash("Category not found", "danger")
        return redirect("/")

    # Pull 10 random questions from this category (or all if fewer than 10)
    questions = db.execute("""
        SELECT id FROM questions WHERE category_id = ?
        ORDER BY RANDOM() LIMIT 10
    """, (category_id,)).fetchall()

    if not questions:
        flash("No questions available in this category yet.", "warning")
        return redirect("/")

    # Store quiz state in session
    session["quiz"] = {
        "category_id": category_id,
        "category_name": category["name"],
        "question_ids": [q["id"] for q in questions],
        "current_index": 0,
        "score": 0,
        "answers": []  # list of {question_id, answer_id, is_correct}
    }

    return redirect("/quiz/question")


@app.route("/quiz/question")
@login_required
def quiz_question():
    """Serve the current question."""
    quiz = session.get("quiz")
    if not quiz:
        return redirect("/")

    idx = quiz["current_index"]
    if idx >= len(quiz["question_ids"]):
        return redirect("/quiz/results")

    question_id = quiz["question_ids"][idx]
    db = get_db()

    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    answers = db.execute(
        "SELECT * FROM answers WHERE question_id = ? ORDER BY RANDOM()",
        (question_id,)
    ).fetchall()

    return render_template("quiz.html",
        question=question,
        answers=answers,
        current=idx + 1,
        total=len(quiz["question_ids"]),
        category_name=quiz["category_name"]
    )


@app.route("/quiz/submit", methods=["POST"])
@login_required
def quiz_submit():
    """
    Submit an answer. Returns JSON so this works as an API endpoint
    for a future mobile app with no changes needed.
    """
    quiz = session.get("quiz")
    if not quiz:
        return jsonify({"error": "No active quiz"}), 400

    answer_id = request.form.get("answer_id", type=int)
    if not answer_id:
        return jsonify({"error": "No answer selected"}), 400

    question_id = quiz["question_ids"][quiz["current_index"]]
    db = get_db()

    # Check if answer is correct
    answer = db.execute("SELECT * FROM answers WHERE id = ?", (answer_id,)).fetchone()
    correct_answer = db.execute(
        "SELECT * FROM answers WHERE question_id = ? AND is_correct = 1",
        (question_id,)
    ).fetchone()
    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()

    is_correct = 1 if answer and answer["is_correct"] else 0

    # Log result to database (powers spaced repetition in Stage 2)
    db.execute("""
        INSERT INTO results (user_id, question_id, answer_id, is_correct)
        VALUES (?, ?, ?, ?)
    """, (session["user_id"], question_id, answer_id, is_correct))
    db.commit()

    # Update session state
    quiz["answers"].append({
        "question_id": question_id,
        "answer_id": answer_id,
        "is_correct": is_correct,
        "correct_answer_text": correct_answer["answer_text"],
        "explanation": question["explanation"]
    })
    if is_correct:
        quiz["score"] += 1
    quiz["current_index"] += 1
    session["quiz"] = quiz
    session.modified = True

    # Return JSON — works for web (via JS) and future mobile app
    return jsonify({
        "is_correct": is_correct,
        "correct_answer_id": correct_answer["id"],
        "correct_answer_text": correct_answer["answer_text"],
        "explanation": question["explanation"],
        "next_url": "/quiz/results" if quiz["current_index"] >= len(quiz["question_ids"]) else "/quiz/question"
    })


@app.route("/quiz/results")
@login_required
def quiz_results():
    """Show end-of-round summary."""
    quiz = session.get("quiz")
    if not quiz:
        return redirect("/")

    score = quiz["score"]
    total = len(quiz["question_ids"])
    percentage = round((score / total) * 100) if total > 0 else 0

    # Fetch full question/answer details for review
    db = get_db()
    review = []
    for entry in quiz["answers"]:
        question = db.execute("SELECT * FROM questions WHERE id = ?", (entry["question_id"],)).fetchone()
        user_answer = db.execute("SELECT * FROM answers WHERE id = ?", (entry["answer_id"],)).fetchone()
        review.append({
            "question_text": question["question_text"],
            "user_answer": user_answer["answer_text"],
            "correct_answer": entry["correct_answer_text"],
            "explanation": entry["explanation"],
            "is_correct": entry["is_correct"],
            "source": question["source"]
        })

    session.pop("quiz", None)  # Clear quiz state
    return render_template("results.html",
        score=score,
        total=total,
        percentage=percentage,
        review=review,
        category_name=quiz["category_name"]
    )


@app.route("/progress")
@login_required
def progress():
    """User progress dashboard."""
    db = get_db()
    stats = db.execute("""
        SELECT
            c.name as category_name,
            COUNT(r.id) as total_answered,
            SUM(r.is_correct) as total_correct,
            ROUND(AVG(r.is_correct) * 100) as accuracy
        FROM results r
        JOIN questions q ON q.id = r.question_id
        JOIN categories c ON c.id = q.category_id
        WHERE r.user_id = ?
        GROUP BY c.id
        ORDER BY c.name
    """, (session["user_id"],)).fetchall()

    overall = db.execute("""
        SELECT COUNT(id) as total, SUM(is_correct) as correct
        FROM results WHERE user_id = ?
    """, (session["user_id"],)).fetchone()

    return render_template("progress.html", stats=stats, overall=overall)


# ─────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect("/admin")
        flash("Invalid admin password", "danger")
    return render_template("admin/login.html")


@app.route("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    question_count = db.execute("SELECT COUNT(*) as n FROM questions").fetchone()["n"]
    user_count = db.execute("SELECT COUNT(*) as n FROM users").fetchone()["n"]
    category_count = db.execute("SELECT COUNT(*) as n FROM categories").fetchone()["n"]
    result_count = db.execute("SELECT COUNT(*) as n FROM results").fetchone()["n"]
    return render_template("admin/dashboard.html",
        question_count=question_count,
        user_count=user_count,
        category_count=category_count,
        result_count=result_count
    )


@app.route("/admin/categories", methods=["GET", "POST"])
@admin_required
def admin_categories():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        icon = request.form.get("icon", "📚")
        if name:
            db.execute("INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)",
                       (name, description, icon))
            db.commit()
            flash(f"Category '{name}' added.", "success")
    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()
    return render_template("admin/categories.html", categories=categories)


@app.route("/admin/questions", methods=["GET", "POST"])
@admin_required
def admin_questions():
    db = get_db()
    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        question_text = request.form.get("question_text")
        explanation = request.form.get("explanation")
        difficulty = request.form.get("difficulty", type=int, default=1)
        source = request.form.get("source")

        # Four answer options, one marked correct
        answers = [
            request.form.get("answer_1"),
            request.form.get("answer_2"),
            request.form.get("answer_3"),
            request.form.get("answer_4"),
        ]
        correct_index = request.form.get("correct_answer", type=int)  # 1-4

        if not all([category_id, question_text, all(answers), correct_index]):
            flash("All fields are required.", "danger")
        else:
            # Insert question
            cursor = db.execute("""
                INSERT INTO questions (category_id, question_text, explanation, difficulty, source)
                VALUES (?, ?, ?, ?, ?)
            """, (category_id, question_text, explanation, difficulty, source))
            question_id = cursor.lastrowid

            # Insert answers
            for i, answer_text in enumerate(answers):
                is_correct = 1 if (i + 1) == correct_index else 0
                db.execute("""
                    INSERT INTO answers (question_id, answer_text, is_correct)
                    VALUES (?, ?, ?)
                """, (question_id, answer_text, is_correct))

            db.commit()
            flash("Question added successfully.", "success")

    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()
    questions = db.execute("""
        SELECT q.*, c.name as category_name,
               COUNT(a.id) as answer_count
        FROM questions q
        JOIN categories c ON c.id = q.category_id
        LEFT JOIN answers a ON a.question_id = q.id
        GROUP BY q.id
        ORDER BY q.created_at DESC
    """).fetchall()

    return render_template("admin/questions.html",
        categories=categories,
        questions=questions
    )


if __name__ == "__main__":
    app.run(debug=True)