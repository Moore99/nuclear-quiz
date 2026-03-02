import json
import os
import secrets
import smtplib
import uuid
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage

import jwt
from flask import Blueprint, g, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import get_db, jwt_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

def _make_token(user_id):
    payload = {
        "sub": str(user_id),  # PyJWT 2.x requires sub to be a string (RFC 7519)
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def _get_quiz_session(db, quiz_id, user_id):
    """Fetch quiz session and verify ownership. Returns (quiz, None) or (None, error_response)."""
    quiz = db.execute("SELECT * FROM quiz_sessions WHERE id = ?", (quiz_id,)).fetchone()
    if not quiz:
        return None, (jsonify({"error": "Quiz not found"}), 404)
    if quiz["user_id"] != user_id:
        return None, (jsonify({"error": "Forbidden"}), 403)
    return quiz, None


def _parse_question_ids(quiz):
    return json.loads(quiz["question_ids"])


# ─────────────────────────────────────────────
# AUTH & ACCOUNT
# ─────────────────────────────────────────────

@api_bp.route("/auth/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400

    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        return jsonify({"error": "Username already taken"}), 409

    pw_hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, pw_hash))
    db.commit()

    user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    token = _make_token(user["id"])
    return jsonify({"token": token, "user_id": user["id"]}), 201


@api_bp.route("/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user or not check_password_hash(user["hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = _make_token(user["id"])
    return jsonify({"token": token, "user_id": user["id"]}), 200


@api_bp.route("/auth/forgot-password", methods=["POST"])
def api_forgot_password():
    """Step 1: request a reset token. Always returns 200 to avoid username enumeration."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"message": "If that account exists, a reset email has been sent."}), 200

    db = get_db()
    user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        return jsonify({"message": "If that account exists, a reset email has been sent."}), 200

    # Invalidate any existing unused tokens for this user
    db.execute("UPDATE password_reset_tokens SET used = 1 WHERE user_id = ? AND used = 0",
               (user["id"],))

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    db.execute(
        "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
        (user["id"], token, expires_at.isoformat())
    )
    db.commit()

    _send_reset_email(username, token)
    return jsonify({"message": "If that account exists, a reset email has been sent."}), 200


@api_bp.route("/auth/reset-password", methods=["POST"])
def api_reset_password():
    """Step 2: consume token and set new password."""
    data = request.get_json(silent=True) or {}
    token = data.get("token", "").strip()
    new_password = data.get("new_password", "")

    if not token or not new_password:
        return jsonify({"error": "token and new_password are required"}), 400
    if len(new_password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400

    db = get_db()
    row = db.execute("""
        SELECT id, user_id, expires_at, used
        FROM password_reset_tokens WHERE token = ?
    """, (token,)).fetchone()

    if not row or row["used"]:
        return jsonify({"error": "Invalid or expired reset token"}), 400

    expires_at = datetime.fromisoformat(row["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        return jsonify({"error": "Reset token has expired"}), 400

    pw_hash = generate_password_hash(new_password)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", (pw_hash, row["user_id"]))
    db.execute("UPDATE password_reset_tokens SET used = 1 WHERE id = ?", (row["id"],))
    db.commit()
    return jsonify({"message": "Password reset successful. You can now log in."}), 200


def _send_reset_email(username: str, token: str):
    """Send password reset email. Silently no-ops if SMTP env vars are not configured."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    from_addr = os.environ.get("SMTP_FROM", smtp_user or "noreply@nuclear-motd.com")
    base_url = os.environ.get("APP_BASE_URL", "https://quiz.nuclear-motd.com")

    if not smtp_host or not smtp_user:
        # Log token to stderr in dev so it can be used without email configured
        import sys
        print(f"[DEV] Password reset token for '{username}': {token}", file=sys.stderr)
        return

    reset_url = f"{base_url}/reset-password?token={token}"
    msg = EmailMessage()
    msg["Subject"] = "Nuclear Quiz — Password Reset"
    msg["From"] = from_addr
    msg["To"] = smtp_user  # In a real app, users would have an email column
    msg.set_content(
        f"Hi {username},\n\n"
        f"You requested a password reset for your Nuclear Quiz account.\n\n"
        f"Reset your password here (link expires in 1 hour):\n{reset_url}\n\n"
        f"If you did not request this, ignore this email.\n\n"
        f"— Nuclear Quiz"
    )
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as s:
            s.starttls()
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
    except Exception as e:
        import sys
        print(f"[WARN] Failed to send reset email: {e}", file=sys.stderr)


@api_bp.route("/auth/change-password", methods=["POST"])
@jwt_required
def api_change_password():
    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    if not current_password or not new_password:
        return jsonify({"error": "current_password and new_password are required"}), 400

    db = get_db()
    user = db.execute("SELECT hash FROM users WHERE id = ?", (g.user_id,)).fetchone()
    if not check_password_hash(user["hash"], current_password):
        return jsonify({"error": "Current password incorrect"}), 401

    pw_hash = generate_password_hash(new_password)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", (pw_hash, g.user_id))
    db.commit()
    return jsonify({"message": "Password updated successful"}), 200


@api_bp.route("/auth/delete-account", methods=["DELETE"])
@jwt_required
def api_delete_account():
    db = get_db()
    # Delete results, sessions, and then the user
    db.execute("DELETE FROM results WHERE user_id = ?", (g.user_id,))
    db.execute("DELETE FROM quiz_sessions WHERE user_id = ?", (g.user_id,))
    db.execute("DELETE FROM users WHERE id = ?", (g.user_id,))
    db.commit()
    return jsonify({"message": "Account deleted forever"}), 200


# ─────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────

@api_bp.route("/categories")
@jwt_required
def api_categories():
    db = get_db()
    rows = db.execute("""
        SELECT c.id, c.name, c.description, c.icon,
               COUNT(q.id) as question_count
        FROM categories c
        LEFT JOIN questions q ON q.category_id = c.id
        GROUP BY c.id
        ORDER BY c.name
    """).fetchall()
    return jsonify([dict(r) for r in rows])


# ─────────────────────────────────────────────
# QUIZ
# ─────────────────────────────────────────────

@api_bp.route("/quiz/start", methods=["POST"])
@jwt_required
def api_quiz_start():
    data = request.get_json(silent=True) or {}
    category_id = data.get("category_id")
    if not category_id:
        return jsonify({"error": "category_id is required"}), 400

    db = get_db()
    category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
    if not category:
        return jsonify({"error": "Category not found"}), 404

    questions = db.execute("""
        SELECT id FROM questions WHERE category_id = ?
        ORDER BY RANDOM() LIMIT 10
    """, (category_id,)).fetchall()
    if not questions:
        return jsonify({"error": "No questions available in this category"}), 404

    quiz_id = str(uuid.uuid4())
    question_ids = json.dumps([q["id"] for q in questions])
    db.execute("""
        INSERT INTO quiz_sessions (id, user_id, category_id, question_ids)
        VALUES (?, ?, ?, ?)
    """, (quiz_id, g.user_id, category_id, question_ids))
    db.commit()

    return jsonify({
        "quiz_id": quiz_id,
        "category_name": category["name"],
        "total_questions": len(questions),
    }), 201


@api_bp.route("/quiz/<quiz_id>")
@jwt_required
def api_quiz_question(quiz_id):
    db = get_db()
    quiz, err = _get_quiz_session(db, quiz_id, g.user_id)
    if err:
        return err

    if quiz["completed"]:
        return jsonify({"error": "Quiz already completed", "is_complete": True}), 410

    question_ids = _parse_question_ids(quiz)
    idx = quiz["current_index"]
    if idx >= len(question_ids):
        return jsonify({"error": "Quiz already complete", "is_complete": True}), 410

    question_id = question_ids[idx]
    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    answers = db.execute(
        "SELECT id, answer_text FROM answers WHERE question_id = ? ORDER BY RANDOM()",
        (question_id,)
    ).fetchall()

    return jsonify({
        "quiz_id": quiz_id,
        "question_number": idx + 1,
        "total_questions": len(question_ids),
        "question_id": question["id"],
        "question_text": question["question_text"],
        "answers": [{"id": a["id"], "answer_text": a["answer_text"]} for a in answers],
    })


@api_bp.route("/quiz/<quiz_id>/answer", methods=["POST"])
@jwt_required
def api_quiz_answer(quiz_id):
    db = get_db()
    quiz, err = _get_quiz_session(db, quiz_id, g.user_id)
    if err:
        return err

    if quiz["completed"]:
        return jsonify({"error": "Quiz already completed"}), 410

    data = request.get_json(silent=True) or {}
    answer_id = data.get("answer_id")
    if not answer_id:
        return jsonify({"error": "answer_id is required"}), 400

    question_ids = _parse_question_ids(quiz)
    idx = quiz["current_index"]
    if idx >= len(question_ids):
        return jsonify({"error": "Quiz already complete"}), 410

    question_id = question_ids[idx]
    answer = db.execute(
        "SELECT * FROM answers WHERE id = ? AND question_id = ?", (answer_id, question_id)
    ).fetchone()
    if not answer:
        return jsonify({"error": "Invalid answer_id for this question"}), 400

    correct_answer = db.execute(
        "SELECT * FROM answers WHERE question_id = ? AND is_correct = 1", (question_id,)
    ).fetchone()
    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()

    is_correct = 1 if answer["is_correct"] else 0
    new_score = quiz["score"] + is_correct
    new_index = idx + 1
    is_complete = new_index >= len(question_ids)

    # Write to results table (shared with web, powers unified progress)
    db.execute("""
        INSERT INTO results (user_id, question_id, answer_id, is_correct)
        VALUES (?, ?, ?, ?)
    """, (g.user_id, question_id, answer_id, is_correct))

    db.execute("""
        UPDATE quiz_sessions
        SET current_index = ?, score = ?, completed = ?
        WHERE id = ?
    """, (new_index, new_score, 1 if is_complete else 0, quiz_id))
    db.commit()

    return jsonify({
        "is_correct": bool(is_correct),
        "correct_answer_id": correct_answer["id"],
        "correct_answer_text": correct_answer["answer_text"],
        "explanation": question["explanation"],
        "score": new_score,
        "questions_answered": new_index,
        "total_questions": len(question_ids),
        "is_complete": is_complete,
    })


@api_bp.route("/quiz/<quiz_id>/results")
@jwt_required
def api_quiz_results(quiz_id):
    db = get_db()
    quiz, err = _get_quiz_session(db, quiz_id, g.user_id)
    if err:
        return err

    question_ids = _parse_question_ids(quiz)
    total = len(question_ids)
    score = quiz["score"]
    percentage = round((score / total) * 100) if total > 0 else 0

    # Reconstruct review from results table (not cached session state)
    review = []
    for qid in question_ids:
        result = db.execute("""
            SELECT r.is_correct, r.answer_id,
                   q.question_text, q.explanation, q.source,
                   a.answer_text as user_answer_text
            FROM results r
            JOIN questions q ON q.id = r.question_id
            JOIN answers a ON a.id = r.answer_id
            WHERE r.user_id = ? AND r.question_id = ?
            ORDER BY r.answered_at DESC
            LIMIT 1
        """, (g.user_id, qid)).fetchone()
        correct = db.execute(
            "SELECT answer_text FROM answers WHERE question_id = ? AND is_correct = 1", (qid,)
        ).fetchone()
        if result:
            review.append({
                "question_text": result["question_text"],
                "user_answer": result["user_answer_text"],
                "correct_answer": correct["answer_text"] if correct else None,
                "explanation": result["explanation"],
                "source": result["source"],
                "is_correct": bool(result["is_correct"]),
            })

    return jsonify({
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "review": review,
    })


# ─────────────────────────────────────────────
# PROGRESS
# ─────────────────────────────────────────────

@api_bp.route("/progress")
@jwt_required
def api_progress():
    db = get_db()
    overall = db.execute("""
        SELECT COUNT(id) as total, SUM(is_correct) as correct
        FROM results WHERE user_id = ?
    """, (g.user_id,)).fetchone()

    by_category = db.execute("""
        SELECT
            c.id as category_id,
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
    """, (g.user_id,)).fetchall()

    total = overall["total"] or 0
    correct = overall["correct"] or 0
    return jsonify({
        "overall": {
            "total_answered": total,
            "total_correct": correct,
            "accuracy": round((correct / total) * 100) if total > 0 else 0,
        },
        "by_category": [dict(r) for r in by_category],
    })
