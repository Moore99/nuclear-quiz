# 🧪 Development Guide - Nuclear Quiz

This guide is for developers working on the Nuclear Quiz project locally.

## 🚀 Local Development Setup

### Prerequisites

- Python 3.11+
- SQLite3
- Docker (for container testing)
- Git

### Initial Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd nuclear_quiz

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file for development
cp .env.example .env
```

### Development .env Configuration

Edit `.env` for local development:

```bash
SECRET_KEY=dev-secret-key-for-testing
ADMIN_PASSWORD=dev-admin-password
FLASK_ENV=development
PORT=5000
DATABASE_PATH=/tmp/nuclear_quiz.db
SESSION_DIR=/tmp/flask_session
```

### Initialize Database

```bash
# Create database and load schema
python init_db.py

# Add sample data
python add_questions.py
```

### Run Development Server

```bash
# Option 1: Flask development server (auto-reload)
python -m flask run

# Option 2: Gunicorn (production-like)
gunicorn app:app --reload --bind 0.0.0.0:5000

# Then open: http://localhost:5000
```

---

## 📱 Web vs API Development

### Web App (Traditional Forms)

**Routes:** `/register`, `/login`, `/account`, `/quiz/*`, `/progress`

```bash
# Test in browser
curl http://localhost:5000/login
```

- Session-based authentication (cookies)
- HTML form submissions
- Server-side rendering with Jinja2

### API (JSON/JWT)

**Routes:** `/api/auth/*`, `/api/quiz/*`, `/api/categories`, `/api/progress`

```bash
# Test with curl
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get JWT token
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq -r '.token')

# Use token for authenticated requests
curl http://localhost:5000/api/categories \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Database Schema

### Tables

```
users              → user accounts & passwords
├─ id (PK)
├─ username (UNIQUE)
├─ hash (password)
└─ created_at

categories         → quiz topics
├─ id (PK)
├─ name
├─ description
└─ icon

questions          → quiz questions
├─ id (PK)
├─ category_id (FK)
├─ question_text
├─ explanation
├─ difficulty
└─ source

answers            → multiple choice options
├─ id (PK)
├─ question_id (FK)
├─ answer_text
└─ is_correct

results            → user responses (analytics)
├─ id (PK)
├─ user_id (FK)
├─ question_id (FK)
├─ answer_id (FK)
├─ is_correct
└─ answered_at

quiz_sessions      → stateless API quiz state
├─ id (PK)
├─ user_id (FK)
├─ category_id (FK)
├─ question_ids (JSON)
├─ current_index
├─ score
├─ completed
└─ created_at
```

### Database Commands

```bash
# Connect to dev database
sqlite3 /tmp/nuclear_quiz.db

# Common queries
> .tables
> SELECT COUNT(*) FROM users;
> SELECT * FROM results WHERE user_id = 1;
> .dump > backup.sql

# Exit
> .quit
```

---

## 🧪 Testing

### Manual Testing Checklist

```
[ ] User Registration
    [ ] Valid username/password creates account
    [ ] Duplicate username rejected
    [ ] Password too short rejected
    
[ ] User Login
    [ ] Valid credentials authenticate
    [ ] Invalid credentials rejected
    
[ ] Quiz Flow
    [ ] Quiz starts with 10 random questions
    [ ] Questions display with shuffled answers
    [ ] Answers are recorded correctly
    [ ] Results show correct scoring
    
[ ] Account Management
    [ ] Change password works
    [ ] Delete account removes all data
    [ ] Session clears after deletion
    
[ ] Admin Panel
    [ ] Password-protected login
    [ ] Session expires after 2 hours
    [ ] Add categories works
    [ ] Add questions with 4 answers works
    [ ] Logout clears admin session
    
[ ] API Endpoints
    [ ] /api/auth/register returns JWT
    [ ] /api/auth/login returns JWT
    [ ] /api/categories requires auth
    [ ] /api/quiz/start creates session
    [ ] /api/quiz/* endpoints work with JWT
```

### API Testing with cURL

```bash
#!/bin/bash

# Create user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq

# Login (save token)
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq -r '.token')

# Get categories
curl http://localhost:5000/api/categories \
  -H "Authorization: Bearer $TOKEN" | jq

# Start quiz
QUIZ=$(curl -X POST http://localhost:5000/api/quiz/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category_id":1}' | jq -r '.quiz_id')

# Get question
curl http://localhost:5000/api/quiz/$QUIZ \
  -H "Authorization: Bearer $TOKEN" | jq

# Submit answer
curl -X POST http://localhost:5000/api/quiz/$QUIZ/answer \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"answer_id":1}' | jq

# Get results
curl http://localhost:5000/api/quiz/$QUIZ/results \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 🐳 Docker Development

### Build & Test Docker Image Locally

```bash
# Build image
docker build -t nuclear-quiz:dev .

# Run container
docker run -p 5001:5000 \
  -e SECRET_KEY=dev-key \
  -e ADMIN_PASSWORD=dev-admin \
  -e FLASK_ENV=development \
  nuclear-quiz:dev

# Test in container
curl http://localhost:5001/
```

### Docker Compose Development

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f quiz

# Shell into container
docker compose exec quiz sh

# Rebuild after code changes
docker compose build && docker compose up -d
```

---

## 🔄 Development Workflow

### Making Changes

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes locally**
   ```bash
   # Edit app.py, api.py, etc.
   ```

3. **Test changes**
   ```bash
   python -m flask run
   # Test manually in browser/with curl
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

### Code Quality Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Use type hints where possible
- Test both web and API routes
- Update error messages to be clear for users

---

## 📝 Common Tasks

### Add New Quiz Questions

The navigation bar has been updated to make it easy to move around:
- **Log In / Register** appear when no user is signed in.
- **My Progress / Account / Logout** replace them when a user is logged in.
- Admins (without a user account) see **Admin Dashboard** and a logout link.
- If you’re both a user and an administrator, you’ll see the normal user
  links plus an **Admin** link to the dashboard.

```bash
# Manual method
python add_questions.py

# Or via admin panel
# 1. Open http://localhost:5000/admin
# 2. Enter admin password
# 3. Click "Manage Questions"
# 4. Fill form and submit
```

### Add New Category

You can add categories/questions in two ways:

```bash
# 1. Run the helper script (mirrors Android content):
python expand_questions.py
# It will prompt for names and questions, appending them to the DB.

# 2. Via admin panel
#    1. Open http://localhost:5000/admin
#    2. Click "Manage Categories"
#    3. Enter category name and description
#    4. Submit
```

### Reset Database

```bash
# Delete and recreate
rm /tmp/nuclear_quiz.db
python init_db.py
python add_questions.py
```

### Debug Issues

```bash
# Check Flask logs
python -m flask run  # Shows all requests

# Database inspection
sqlite3 /tmp/nuclear_quiz.db "SELECT * FROM users;"

# Check session files
ls -la /tmp/flask_session/
```

---

## 🔐 Security During Development

**DO:**
- Use different SECRET_KEY for development
- Use weak ADMIN_PASSWORD for dev only
- Keep .env in .gitignore
- Test with invalid inputs
- Validate all form inputs

**DON'T:**
- Commit .env to git
- Use production passwords locally
- Share credentials in commit messages
- Hard-code secrets in code
- Leave debug=True in production

---

## 📚 File Structure

```
nuclear_quiz/
├── app.py                    # Main Flask app (web routes)
├── api.py                    # REST API routes
├── helpers.py                # Auth decorators, DB utilities
├── schema.sql                # Database schema
├── requirements.txt          # Python dependencies
├── init_db.py               # Database initialization
├── add_questions.py         # Seed data loader
│
├── templates/
│   ├── layout.html          # Base template
│   ├── index.html           # Home/categories
│   ├── quiz.html            # Quiz interface
│   ├── results.html         # Quiz results
│   ├── account.html         # Account management
│   ├── progress.html        # User statistics
│   └── admin/
│       ├── login.html       # Admin login
│       ├── dashboard.html   # Admin dashboard
│       ├── categories.html  # Manage categories
│       └── questions.html   # Manage questions
│
├── static/
│   └── styles.css          # Styling
│
├── .github/
│   └── workflows/
│       └── test.yml        # CI/CD pipeline
│
├── .gitignore              # Git ignore rules (CRITICAL)
├── .dockerignore           # Docker ignore rules
├── .env.example            # Environment template
├── Dockerfile              # Container definition
├── docker-compose.yml      # Compose orchestration
├── DEPLOYMENT.md           # Deployment guide
├── DEVELOPMENT.md          # This file
└── README.md               # Project overview
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'flask'" | Run `pip install -r requirements.txt` |
| "Database file is locked" | Close other SQLite connections |
| "Port 5000 already in use" | Use different port: `python -m flask run --port=5001` |
| "Admin session won't expire" | Check `admin_timeout` is set correctly in session |
| "Questions not showing in quiz" | Verify category has questions: `sqlite3 .../db "SELECT COUNT(*) FROM questions WHERE category_id=1;"` |
| ".env file not being loaded" | Ensure `.env` is in project root, not in a subfolder |

---

## 📞 Getting Help

- Check existing issues on GitHub
- Review Flask documentation: https://flask.palletsprojects.com
- Test with simple curl commands first
- Add debug prints to understand flow

---

**Happy coding!** 🚀

