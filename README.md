# Nuclear Industry Quiz

A web-based quiz application for nuclear industry professionals and students, built with Python/Flask. Covers Canadian nuclear regulatory topics, CANDU reactor systems, IAEA safety standards, radiation protection, and nuclear security.

Submitted as the final project for Harvard CS50x.

---

## Video Demo

<!-- Add your CS50 video URL here -->

---

## Description

The Nuclear Industry Quiz allows registered users to test their knowledge across five topic categories drawn from real regulatory documents and IAEA safety standards. After each quiz round, users see an explanation for every question alongside the correct answer — reinforcing learning rather than just scoring. A progress dashboard tracks accuracy by category over time.

An admin interface allows question and category management without touching the database directly.

The application follows the CS50 Finance pattern: Flask + SQLite + Jinja2 templates, with session-based authentication.

---

## How to Run

**Requirements:** Python 3.10+

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize the database (creates nuclear_quiz.db and seeds questions)
python init_db.py

# 3. Run the development server
flask run
```

Open http://127.0.0.1:5000 in your browser. Register an account to begin.

**Admin access:** navigate to `/admin/login`. Default password: `admin123`
(Change via the `ADMIN_PASSWORD` environment variable in production.)

---

## File Structure

### Python

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application. Defines all routes: auth, quiz flow, progress, admin. |
| `helpers.py` | `login_required` and `admin_required` decorators; `get_db()` database helper. |
| `init_db.py` | Creates the SQLite schema and seeds sample questions. Run once on setup. |
| `add_questions.py` | Script used to add the first batch of additional questions to the database. |
| `expand_questions.py` | Script used to add the second batch of additional questions. |

### Database

| File | Purpose |
|------|---------|
| `schema.sql` | SQL schema: `users`, `categories`, `questions`, `answers`, `results` tables. |
| `nuclear_quiz.db` | Pre-seeded SQLite database included for convenience (regenerate with `init_db.py`). |

### Templates

| File | Purpose |
|------|---------|
| `layout.html` | Base template with navbar and flash message display. |
| `index.html` | Home page: category cards with question counts. |
| `login.html` / `register.html` | Authentication pages. |
| `quiz.html` | Question display with four answer choices; submits via JavaScript fetch. |
| `results.html` | End-of-round summary: score, percentage, and per-question review with explanations. |
| `progress.html` | User progress dashboard: accuracy per category and overall stats. |
| `admin/login.html` | Admin password prompt. |
| `admin/dashboard.html` | Admin overview: counts of questions, categories, users, results. |
| `admin/categories.html` | Add and list categories. |
| `admin/questions.html` | Add questions with four answer options. |

### Static

| File | Purpose |
|------|---------|
| `static/styles.css` | Custom CSS layered on top of Bootstrap 5 (loaded via CDN). |

---

## Design Decisions

### Quiz answer submission via JavaScript fetch
Rather than a full page reload on each answer, `quiz.html` submits to `/quiz/submit` via `fetch()` and receives JSON. This powers the immediate feedback overlay (correct/incorrect + explanation) before advancing. It also means the same `/quiz/submit` endpoint can serve a future mobile app without any changes — the JSON contract is already in place.

### Session-stored quiz state
Active quiz state (question IDs, current index, score) lives in the Flask session rather than the database. This avoids partial-completion rows in the database and keeps the quiz logic simple. Results are only written to the `results` table when an answer is submitted, not at end-of-round.

### Explanations on every question
Each question stores an `explanation` field drawn from the source document. Showing the explanation immediately after answering — whether right or wrong — is the core learning mechanism. The results page repeats all explanations in a full review.

### `source` field on questions
Every question links to the specific IAEA or CNSC document it is drawn from (e.g., `CNSC REGDOC-2.4.1`, `IAEA SSR-2/1`). This lets users go directly to the authoritative source, which is important in a regulatory context.

### Admin via password, not user role
Admin access uses a separate password stored in an environment variable rather than a role column on the `users` table. This keeps the user model simple for the CS50 scope and avoids the complexity of role management for a single-admin application.

### Bootstrap 5 via CDN
Styling uses Bootstrap 5 loaded from CDN to keep the repository small and the setup simple. A thin `styles.css` provides overrides and quiz-specific layout.
