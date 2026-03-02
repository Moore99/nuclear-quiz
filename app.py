import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, admin_required, get_db, ensure_quiz_sessions_table
from api import api_bp

# Configure application
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.environ.get(
    "SESSION_DIR",
    "/tmp/flask_session"
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
Session(app)

# Register API Blueprint and CORS (web routes are unaffected)
app.register_blueprint(api_bp)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Create quiz_sessions table if it doesn't exist yet (safe on every startup)
with app.app_context():
    _db = get_db()
    ensure_quiz_sessions_table(_db)
    _db.close()

print("APP STARTED OK")

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
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                flash("Must provide username and password", "danger")
                return render_template("login.html")

            db = get_db()
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

            if not user:
                flash("Invalid username or password", "danger")
                return render_template("login.html")

            if not check_password_hash(user["hash"], password):
                flash("Invalid username or password", "danger")
                return render_template("login.html")

            # grant user session and propagate admin status from database
            session["user_id"] = user["id"]
            if user["is_admin"]:
                session["is_admin"] = True
                session["admin_login_time"] = datetime.now().isoformat()
                session["admin_timeout"] = (datetime.now() + timedelta(hours=2)).isoformat()
            # Force session to be saved
            session.modified = True
            return redirect("/")

        return render_template("login.html")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ─────────────────────────────────────────────
# ACCOUNT MANAGEMENT
# ─────────────────────────────────────────────

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        action = request.form.get("action")
        db = get_db()

        if action == "change_password":
            current_pw = request.form.get("current_password")
            new_pw = request.form.get("new_password")
            confirm_pw = request.form.get("confirm_password")

            user = db.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],)).fetchone()
            if not check_password_hash(user["hash"], current_pw):
                flash("Current password incorrect", "danger")
            elif new_pw != confirm_pw:
                flash("New passwords do not match", "danger")
            elif len(new_pw) < 6:
                flash("New password too short", "danger")
            else:
                new_hash = generate_password_hash(new_pw)
                db.execute("UPDATE users SET hash = ? WHERE id = ?", (new_hash, session["user_id"]))
                db.commit()
                flash("Password changed successfully!", "success")

        elif action == "delete_account":
            db.execute("DELETE FROM results WHERE user_id = ?", (session["user_id"],))
            db.execute("DELETE FROM quiz_sessions WHERE user_id = ?", (session["user_id"],))
            db.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))
            db.commit()
            session.clear()
            flash("Account deleted permanently.", "info")
            return redirect(url_for("login"))

    return render_template("account.html")


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
    db = get_db()
    category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
    if not category:
        flash("Category not found", "danger")
        return redirect("/")

    questions = db.execute("""
        SELECT id FROM questions WHERE category_id = ?
        ORDER BY RANDOM() LIMIT 10
    """, (category_id,)).fetchall()

    if not questions:
        flash("No questions available in this category yet.", "warning")
        return redirect("/")

    session["quiz"] = {
        "category_id": category_id,
        "category_name": category["name"],
        "question_ids": [q["id"] for q in questions],
        "current_index": 0,
        "score": 0,
        "answers": []
    }

    return redirect("/quiz/question")


@app.route("/quiz/question")
@login_required
def quiz_question():
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
    quiz = session.get("quiz")
    if not quiz:
        return jsonify({"error": "No active quiz"}), 400

    answer_id = request.form.get("answer_id", type=int)
    if not answer_id:
        return jsonify({"error": "No answer selected"}), 400

    question_id = quiz["question_ids"][quiz["current_index"]]
    db = get_db()

    answer = db.execute("SELECT * FROM answers WHERE id = ?", (answer_id,)).fetchone()
    correct_answer = db.execute(
        "SELECT * FROM answers WHERE question_id = ? AND is_correct = 1",
        (question_id,)
    ).fetchone()
    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()

    is_correct = 1 if answer and answer["is_correct"] else 0

    db.execute("""
        INSERT INTO results (user_id, question_id, answer_id, is_correct)
        VALUES (?, ?, ?, ?)
    """, (session["user_id"], question_id, answer_id, is_correct))
    db.commit()

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
    quiz = session.get("quiz")
    if not quiz:
        return redirect("/")

    score = quiz["score"]
    total = len(quiz["question_ids"])
    percentage = round((score / total) * 100) if total > 0 else 0

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

    session.pop("quiz", None)
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
# LEGAL PAGES (public — required by app stores)
# ─────────────────────────────────────────────

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/reset-password", methods=["GET", "POST"])
def web_reset_password():
    """Web landing page for password reset links sent via email."""
    token = request.args.get("token") or request.form.get("token", "")

    if request.method == "GET":
        # Validate token so we can show the form or an error
        valid = False
        if token:
            from datetime import timezone as _tz
            db = get_db()
            row = db.execute("""
                SELECT expires_at, used FROM password_reset_tokens WHERE token = ?
            """, (token,)).fetchone()
            if row and not row["used"]:
                exp = datetime.fromisoformat(row["expires_at"])
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=_tz.utc)
                valid = datetime.now(_tz.utc) <= exp
        return render_template("reset_password.html", token=token, token_valid=valid)

    # POST — consume token
    new_password = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")
    if new_password != confirm:
        flash("Passwords do not match", "danger")
        return redirect(url_for("web_reset_password", token=token))
    if len(new_password) < 6:
        flash("Password must be at least 6 characters", "danger")
        return redirect(url_for("web_reset_password", token=token))

    from datetime import timezone as _tz
    db = get_db()
    row = db.execute("""
        SELECT id, user_id, expires_at, used FROM password_reset_tokens WHERE token = ?
    """, (token,)).fetchone()

    if not row or row["used"]:
        flash("Invalid or already-used reset link.", "danger")
        return redirect(url_for("login"))

    exp = datetime.fromisoformat(row["expires_at"])
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=_tz.utc)
    if datetime.now(_tz.utc) > exp:
        flash("Reset link has expired. Please request a new one.", "danger")
        return redirect(url_for("login"))

    from werkzeug.security import generate_password_hash as _gph
    db.execute("UPDATE users SET hash = ? WHERE id = ?",
               (_gph(new_password), row["user_id"]))
    db.execute("UPDATE password_reset_tokens SET used = 1 WHERE id = ?", (row["id"],))
    db.commit()
    flash("Password reset successfully. You can now log in.", "success")
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin authentication with session timeout (2 hours)."""
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            flash("Password is required", "danger")
            return render_template("admin/login.html")
            
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            # Set admin session expiration (2 hours from now)
            session["admin_login_time"] = datetime.now().isoformat()
            session["admin_timeout"] = (datetime.now() + timedelta(hours=2)).isoformat()
            session.modified = True
            flash("Admin access granted", "success")
            return redirect("/admin")
        else:
            flash("Invalid admin password", "danger")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    """Logout from admin panel."""
    session.pop("is_admin", None)
    session.pop("admin_login_time", None)
    session.pop("admin_timeout", None)
    session.modified = True
    flash("Admin session ended", "info")
    return redirect("/admin/login")


@app.route("/admin")
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics."""
    db = get_db()
    question_count = db.execute("SELECT COUNT(*) as n FROM questions").fetchone()["n"]
    user_count = db.execute("SELECT COUNT(*) as n FROM users").fetchone()["n"]
    category_count = db.execute("SELECT COUNT(*) as n FROM categories").fetchone()["n"]
    result_count = db.execute("SELECT COUNT(*) as n FROM results").fetchone()["n"]
    
    # Get admin session info
    admin_timeout_str = session.get("admin_timeout")
    admin_timeout = None
    if admin_timeout_str:
        admin_timeout = datetime.fromisoformat(admin_timeout_str)
    
    return render_template("admin/dashboard.html",
        question_count=question_count,
        user_count=user_count,
        category_count=category_count,
        result_count=result_count,
        admin_timeout=admin_timeout
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

        answers = [
            request.form.get("answer_1"),
            request.form.get("answer_2"),
            request.form.get("answer_3"),
            request.form.get("answer_4"),
        ]
        correct_index = request.form.get("correct_answer", type=int)

        if not all([category_id, question_text, all(answers), correct_index]):
            flash("All fields are required.", "danger")
        else:
            cursor = db.execute("""
                INSERT INTO questions (category_id, question_text, explanation, difficulty, source)
                VALUES (?, ?, ?, ?, ?)
            """, (category_id, question_text, explanation, difficulty, source))
            question_id = cursor.lastrowid

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


@app.route("/admin/backup")
@admin_required
def admin_backup():
    """Download a snapshot of the database as a .db file."""
    import shutil, tempfile
    db_path = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")
    )
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    # Use SQLite online backup API via a temporary connection so the file is
    # consistent even if there are concurrent writes.
    import sqlite3 as _sqlite3
    src = _sqlite3.connect(db_path)
    dst = _sqlite3.connect(tmp.name)
    src.backup(dst)
    dst.close()
    src.close()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nuclear_quiz_backup_{timestamp}.db"
    return send_file(tmp.name, as_attachment=True, download_name=filename,
                     mimetype="application/octet-stream")


if __name__ == "__main__":
    app.run(debug=True)
