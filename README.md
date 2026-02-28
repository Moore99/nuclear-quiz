# 🎯 Nuclear Quiz - Multi-Platform Educational App

[![GitHub Actions](https://github.com/yourusername/nuclear_quiz/workflows/CI/CD%20-%20Test%20%26%20Validate/badge.svg)](https://github.com/yourusername/nuclear_quiz/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-darkgreen.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A comprehensive nuclear energy quiz platform with **web app**, **REST API**, and **Android/iOS mobile app**.

Built with:
- 🐍 **Backend**: Python Flask + SQLite
- 🌐 **Web**: Bootstrap 5 + Jinja2
- 📱 **Mobile**: Kotlin Multiplatform Compose
- 🐳 **Deployment**: Docker + Nginx
- ✅ **CI/CD**: GitHub Actions

---

## 📋 Quick Links

- **Live Demo**: https://quiz.nuclear-motd.com
- **API Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Development Guide**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Docker Setup**: See [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

## ⚡ Quick Start

### Option 1: Docker (Recommended for Production)

```bash
# 1. Clone repository
git clone <repo-url>
cd nuclear_quiz

# 2. Create environment configuration
cp .env.example .env
# Edit .env with your settings

# 3. Run with Docker Compose
docker compose up -d

# 4. Access the app
# Web: http://localhost:5001
# Admin: http://localhost:5001/admin
```

### Option 2: Local Development

```bash
# 1. Clone and setup
git clone <repo-url>
cd nuclear_quiz
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_db.py

# 4. Configure development environment
cp .env.example .env
# Edit .env for development

# 5. Run Flask dev server
python -m flask run

# 6. Access the app
# http://localhost:5000
```

---

## 🎓 Features

### For Users 👥

✅ **User Accounts**
- Secure registration and login
- Password management (change/reset)
- Account deletion with data cleanup
- Session-based authentication
- **Navigation:** once signed in a row of links appears in the navbar — **My Progress**, **Account**, and **Logout** for regular users. Admins see **Admin Dashboard** (and logout) instead, with an extra Admin link if they also have a user account.

✅ **Quizzes & Content**
- 10-question quizzes by category
- Randomized answers with instant feedback
- If a category shows “Coming Soon”, run `python expand_questions.py` or use the admin panel to add both categories and questions. This mirrors the Android data loader and keeps datasets in sync.

✅ **Quiz System**
- 10-question quizzes by category
- Randomized answers
- Immediate feedback with explanations
- Performance tracking

✅ **Progress Tracking**
- Overall statistics
- Per-category performance
- Accuracy percentages
- Historical results review

### For Administrators 🔐

✅ **Admin Panel**
- Protected admin authentication (2-hour sessions)
- Admin identity now linked to user accounts: `is_admin` flag in users table
- Dashboard with statistics
- Question management (CRUD)
- Category management
- User statistics overview

✅ **Content Management**
- Add/edit questions with explanations
- Set difficulty levels
- Manage categories
- Track question sources

### For Developers 👨‍💻

✅ **REST API**
- JWT-based authentication
- Full quiz functionality via API
- Progress/stats endpoints
- Mobile-friendly responses

✅ **DevOps**
- Docker containerization
- GitHub Actions CI/CD
- Automated secrets detection
- Database persistence
- Zero-downtime deployment

---

## 🏗️ Architecture

### Backend Stack

```
┌─────────────────────────────────────────┐
│         Flask Application               │
├─────────────────────────────────────────┤
│  app.py          │  API (api.py)        │
│  Web Routes      │  JSON Endpoints      │
│  Forms-based     │  JWT-secured         │
└─────────────────────────────────────────┘
         ├──────────────────┤
         │  helpers.py      │
         │  - Auth          │
         │  - DB utils      │
         └──────────────────┘
                 ↓
      ┌──────────────────────┐
      │   SQLite Database    │
      │  - Users             │
      │  - Questions         │
      │  - Results           │
      │  - Quiz Sessions     │
      └──────────────────────┘
```

### Authentication

**Web Session (Forms)**
```
User → Login Form → Flask Session → Cookie → Protected Routes
```

**API JWT (Mobile/External)**
```
Client → POST /api/auth/login → Server generates JWT → Bearer token → Protected API endpoints
```

### Database

SQLite with the following tables:
- `users` - User accounts
- `categories` - Quiz categories
- `questions` - Quiz questions
- `answers` - Multiple choice options
- `results` - User performance tracking
- `quiz_sessions` - Stateless API quiz state

---

## 🚀 Deployment

### Production Checklist

- [ ] Strong `SECRET_KEY` generated
- [ ] Strong `ADMIN_PASSWORD` set
- [ ] `.env` file created and secured
- [ ] Docker image built and tested
- [ ] Nginx reverse proxy configured
- [ ] Database backups automated
- [ ] HTTPS/SSL configured (via nginx)
- [ ] Logs monitored
- [ ] Admin session timeout working

### Using Docker Compose

```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f quiz

# Backup database
docker run --rm -v nuclear_quiz_quiz_data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /data .

# Restart
docker compose restart quiz

# Stop
docker compose down
```

### Nginx Configuration

See `deployment/nginx-nuclear-quiz.conf` for production-ready reverse proxy setup.

```nginx
server {
    server_name quiz.nuclear-motd.com;
    location / {
        proxy_pass http://localhost:5001;
        # ... headers ...
    }
}
```

---

## 🔐 Security

### Secrets Management

**NEVER commit:**
- `.env` file (contains SECRET_KEY, ADMIN_PASSWORD)
- `*.db` files (contains user data)
- `flask_session/` directory

**Always:**
- Use strong, randomly generated secrets
- Rotate secrets regularly
- Use environment variables
- Keep production values separate

See [DEPLOYMENT.md#security](DEPLOYMENT.md#-security--secrets--configuration) for complete security guide.

### Automated Security Checks

GitHub Actions verifies:
- ✅ No hardcoded secrets
- ✅ No committed .env files
- ✅ Dependencies vulnerability scan
- ✅ Python syntax checks

---

## 📱 Mobile App (Kotlin Multiplatform)

The `android/` directory contains a production-ready mobile app:
- **Status**: Development/Testing
- **Architecture**: Kotlin Multiplatform Compose
- **Targets**: Android 12+ & iOS 13+
- **Features**: Full quiz functionality, biometric auth, AdMob ads, IAP

See [devbranchreadme.md](devbranchreadme.md) for complete mobile documentation.

---

## 📊 API Reference

### Authentication

```bash
# Register
POST /api/auth/register
Content-Type: application/json
{"username":"user","password":"pass123"}

# Login
POST /api/auth/login
Content-Type: application/json
{"username":"user","password":"pass123"}
→ Returns: { "token": "eyJ...", "user_id": 1 }

# Change Password
POST /api/auth/change-password
Authorization: Bearer <token>
Content-Type: application/json
{"current_password":"old","new_password":"new"}
```

### Quiz

```bash
# Get Categories
GET /api/categories
Authorization: Bearer <token>

# Start Quiz
POST /api/quiz/start
Authorization: Bearer <token>
{"category_id": 1}
→ Returns: { "quiz_id": "uuid", "total_questions": 10 }

# Get Question
GET /api/quiz/{quiz_id}
Authorization: Bearer <token>

# Submit Answer
POST /api/quiz/{quiz_id}/answer
Authorization: Bearer <token>
{"answer_id": 123}

# Get Results
GET /api/quiz/{quiz_id}/results
Authorization: Bearer <token>
```

### Progress

```bash
GET /api/progress
Authorization: Bearer <token>
→ Returns: { "overall": {...}, "by_category": [...] }
```

---

## 🛠️ Development

### Setup Local Environment

```bash
git clone <repo>
cd nuclear_quiz
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python init_db.py
python -m flask run
```

### Run Tests

```bash
# Syntax validation
python -m py_compile app.py api.py helpers.py

# Security checks
pip install bandit
bandit -r app.py api.py helpers.py

# Database validation
sqlite3 :memory: < schema.sql
```

For complete development guide, see [DEVELOPMENT.md](DEVELOPMENT.md).

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| Python Files | 7 (app, api, helpers, init, scripts) |
| HTML Templates | 10 |
| Database Tables | 6 |
| API Endpoints | 17 |
| Lines of Code | ~1800 |
| Test Coverage | ✅ CI/CD verified |
| Docker Size | ~120MB |

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make changes and test locally**
4. **Commit with clear messages**: `git commit -m "feat: add my feature"`
5. **Push to your fork**: `git push origin feature/my-feature`
6. **Create a Pull Request**

All PRs are automatically tested by GitHub Actions before review.

### Code Style

- Follow PEP 8 for Python
- Use type hints
- Add docstrings to functions
- Test both web and API routes
- Update relevant documentation

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment, Docker, secrets management
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Local setup, testing, development workflow
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker containerization details
- **[devbranchreadme.md](devbranchreadme.md)** - Mobile app (Kotlin) documentation

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Port already in use" | Change PORT in .env or use different port |
| "Database locked" | Close other sqlite connections |
| "SECRET_KEY not set" | Create .env from .env.example |
| "Admin session expires immediately" | Check admin_timeout datetime parsing |
| "No questions in quiz" | Verify category_id has questions in DB |

### Debug Mode

```bash
# Enable Flask debug mode (development only)
FLASK_ENV=development FLASK_DEBUG=1 python -m flask run
```

### View Logs

```bash
# Docker logs
docker compose logs -f quiz

# Database inspection
sqlite3 /tmp/nuclear_quiz.db ".tables"
sqlite3 /tmp/nuclear_quiz.db "SELECT * FROM users;"
```

---

## ✅ Testing Checklist

- [ ] User registration works
- [ ] Login/logout functionality
- [ ] Quiz flow (10 random questions)
- [ ] Answer submission and scoring
- [ ] Progress tracking
- [ ] Account management (password change, deletion)
- [ ] Admin panel access control
- [ ] Admin session timeout (2 hours)
- [ ] API endpoints with JWT
- [ ] Docker image builds and runs
- [ ] Database persists after restart

---

## 📞 Support

- 🐛 **Issues**: Create a GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: [contact info]
- 📖 **Docs**: See documentation files

---

## 📄 License

[Your License Here] - See LICENSE file for details

---

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for UI components
- Kotlin Multiplatform community
- All contributors

---

## 🗺️ Roadmap

- [ ] Email-based password reset
- [ ] Leaderboard system
- [ ] Badge/achievement system
- [ ] Question difficulty filtering
- [ ] Export quiz results as PDF
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

---

**Last Updated**: February 28, 2026

For the latest updates, see [CHANGELOG.md](CHANGELOG.md) (if available).

