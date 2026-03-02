# CLAUDE.md — Nuclear Quiz Project Guide for AI Assistants

Read this file first. It reflects the actual current state of the codebase, not the original plans.

---

## Project Overview

Flask web app + Compose Multiplatform (CMP/KMP) mobile app sharing one backend database.

- **Web**: Flask, deployed at https://quiz.nuclear-motd.com
- **Mobile**: Compose Multiplatform (Kotlin, NOT Flutter), in `android/` subdirectory
- **Backend**: SQLite via Flask, JWT-protected REST API at `/api/`
- **Server**: nuclear-motd.com, Docker-managed

---

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `development` | Active development (current) |
| `docker` | Production deployment on server |
| `main` | CS50 submission — frozen, do not modify |

**When making changes**: work on `development`. Merge to `docker` for production.
**The `docker` branch may lag behind** `development` — check before assuming production is up to date.

---

## Tech Stack — Accurate Reference

### Web (Flask)
- Python 3.11, Flask, Flask-Session, Flask-CORS
- Auth: session-based (web), JWT (API)
- DB: SQLite (`nuclear_quiz.db`)
- Templates: Jinja2 + Bootstrap 5.3
- Bootstrap Icons are NOT included — Font Awesome CDN is referenced in templates but missing from `layout.html` (known bug)

### Mobile (Compose Multiplatform — NOT Flutter)
- Kotlin 2.0.21, CMP 1.7.3
- HTTP: Ktor 3.0.3 with OkHttp (Android) / Darwin (iOS) engines
- Serialization: kotlinx.serialization 1.7.3
- Pattern: MVVM, StateFlow, `AppDependencies` singleton (no Hilt/DI framework)
- Navigation: type-safe nav with `@Serializable` route objects
- Token storage: `TokenStore` interface (Android: `EncryptedSharedPreferences`; iOS: `NSUserDefaults` — needs Keychain for production)
- Module: `android/composeApp/`
- Min SDK: 26, Target SDK: 35

**Note**: `devbranchreadme.md` in the repo root describes a Flutter app that was never built. Ignore it. The actual app is CMP.

---

## File Map — Key Files

```
app.py              Web routes + admin routes
api.py              REST API (JWT-protected, used by mobile)
helpers.py          login_required, admin_required, jwt_required, get_db
schema.sql          Database schema (source of truth)
templates/
  layout.html       Base template — navbar logic lives here
  account.html      Password change + account deletion (web)
  admin/            Admin panel templates
android/
  composeApp/src/
    commonMain/     Shared Kotlin code (screens, ViewModels, API models)
    androidMain/    Android-specific (MainActivity, HttpClient, TokenStore)
    iosMain/        iOS-specific (MainViewController, HttpClient, TokenStore)
```

---

## Database Schema (concise)

```sql
users      (id, username, hash, is_admin, created_at)
categories (id, name, description, icon)
questions  (id, category_id, question_text, explanation, difficulty, source, created_at)
answers    (id, question_id, answer_text, is_correct)
results    (id, user_id, question_id, answer_id, is_correct, answered_at)
quiz_sessions (id, user_id, category_id, question_ids, current_index, score, completed, created_at)
```

Account deletion must cascade: delete results, quiz_sessions, then users.

---

## API Contract (summary)

All mobile API endpoints are under `/api/`. Auth endpoints return `{"token": "...", "user_id": N}`.

| Method | Endpoint | Auth | Notes |
|--------|----------|------|-------|
| POST | `/api/auth/register` | None | Returns token + user_id |
| POST | `/api/auth/login` | None | Returns token + user_id |
| POST | `/api/auth/change-password` | JWT | Requires current_password + new_password |
| DELETE | `/api/auth/delete-account` | JWT | Cascades: results → quiz_sessions → users |
| GET | `/api/categories` | JWT | Returns id, name, description, icon, question_count |
| POST | `/api/quiz/start` | JWT | Body: {category_id} |
| GET | `/api/quiz/<quiz_id>` | JWT | Current question |
| POST | `/api/quiz/<quiz_id>/answer` | JWT | Body: {answer_id} |
| GET | `/api/quiz/<quiz_id>/results` | JWT | Score + review items |
| GET | `/api/progress` | JWT | Overall + by-category stats |

**Password reset**: No secure password reset endpoint exists yet. A proper email-token flow is on the roadmap. The previous unauthenticated reset endpoint was removed (security hole — it allowed anyone to reset anyone's password).

---

## Admin Authentication

Two admin auth paths exist:

1. **Admin panel login** (`/admin/login`): Uses `ADMIN_PASSWORD` env var. Sets `session["is_admin"]` + 2-hour timeout. No `user_id` set.
2. **DB admin via regular login** (`/login`): If `users.is_admin = 1`, sets both `session["user_id"]` and `session["is_admin"]`. No timeout set (security gap — known issue).

The `admin_required` decorator in `helpers.py` enforces the session check and timeout.

---

## Known Issues (as of 2026-03-01)

| # | Issue | File | Status |
|---|-------|------|--------|
| 1 | Font Awesome CSS missing from layout.html | `templates/layout.html` | Open |
| 2 | Admin timeout not set for DB admins logging in via /login | `app.py:104` | Open |
| 3 | iOS TokenStore uses NSUserDefaults instead of Keychain | `iosMain/.../IosTokenStore.kt` | Open |
| 4 | Dead code: `session.get('account_success')` never set | `templates/account.html:58` | Open |
| 5 | Mobile Category model missing description/icon fields | `ApiModels.kt` | Open |
| 6 | devbranchreadme.md is stale (describes Flutter, not CMP) | `devbranchreadme.md` | Open |
| 7 | docker branch may lag behind development | git | Open |

---

## What Is Fully Implemented

- User registration, login, logout (web + API)
- Quiz flow (web + API)
- Progress tracking (web + API)
- Account management: change password (web + mobile)
- Account deletion (web + mobile) — cascades correctly on all platforms
- Admin panel: login, logout, session timeout, categories, questions
- Admin authentication with 2-hour auto-timeout

---

## What Is NOT Yet Implemented

- Password reset via email (endpoint removed; proper flow needed with token + email)
- AdMob integration
- Firebase Analytics / Crashlytics
- In-app purchases
- Database backup endpoints
- Keychain-backed iOS token storage (prototype uses NSUserDefaults)
- Privacy policy / terms pages at `/quiz/privacy-policy` and `/quiz/terms`

---

## Testing

### Web
```bash
# Local (no Docker)
python -m flask run

# Docker
docker compose up -d
docker compose logs -f quiz
```

### Android
Open `android/` in Android Studio → Gradle sync → Run on emulator or device.

### iOS framework (verify it builds)
Use Codemagic — iOS KMP targets cannot compile on Windows. Trigger a Codemagic build to verify both Android and iOS.

### Key test scenarios
- Register → login → take quiz → check progress
- Change password (web and mobile)
- Delete account → confirm cascade → redirect to login
- Admin login via `/admin/login` → verify 2-hour session info shown
- Admin logout → verify session cleared

---

## Security Notes

- `SECRET_KEY` and `ADMIN_PASSWORD` must be set as env vars in production. Defaults in code are dev-only.
- JWT tokens expire in 30 days.
- Passwords are hashed with Werkzeug (pbkdf2:sha256).
- Flask-CORS is enabled for `/api/*` only.
- DB files and `.env` are excluded from git via `.gitignore`.
