# Nuclear Quiz - Deployment & Secrets Management Guide

## 🔐 Security: Secrets & Configuration

### Environment Variables

Your application uses the following sensitive configuration via environment variables:

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `SECRET_KEY` | Flask session & JWT signing | `change-this-secret-key` | ✅ Yes |
| `ADMIN_PASSWORD` | Admin panel authentication | `changeme` | ✅ Yes |
| `FLASK_ENV` | App mode (production/development) | `production` | ✅ Yes |
| `PORT` | Host port mapping | `5001` | ❌ No |
| `DATABASE_PATH` | SQLite database location | `/data/nuclear_quiz.db` | ❌ No |
| `SESSION_DIR` | Flask session storage | `/data/flask_session` | ❌ No |

### 🚨 CRITICAL SECURITY NOTES

1. **NEVER commit `.env` files to GitHub**
   - Use `.env.example` as a template
   - Each environment (dev, staging, prod) gets its own `.env`
   - Rotate `SECRET_KEY` and `ADMIN_PASSWORD` regularly

2. **Generate Strong Secrets**
   ```bash
   # Generate a secure SECRET_KEY (64 hex characters = 32 bytes)
   python3 -c "import secrets; print(secrets.token_hex(32))"
   
   # Generate a strong ADMIN_PASSWORD
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Database Files**
   - Never commit `*.db` files to GitHub
   - SQLite databases contain user credentials and quiz data
   - The `.gitignore` already excludes all `.db` files

4. **Session Files**
   - `flask_session/` directory is ignored by git
   - Contains user session data
   - Should be cleared regularly or moved to a distributed store in production

---

## 🐳 Docker Deployment

### Quick Start

```bash
# 1. Create .env from template
cp .env.example .env

# 2. Edit .env with your secrets
nano .env  # or use your editor
# Set:
# - SECRET_KEY to a strong random value
# - ADMIN_PASSWORD to a strong password
# - FLASK_ENV to production
# - PORT to your desired port (e.g., 5001)

# 3. Build and run
docker compose up -d

# 4. Verify
docker compose ps
docker compose logs -f quiz
```

### Production Checklist

- [ ] Set strong `SECRET_KEY` (at least 32 bytes)
- [ ] Set strong `ADMIN_PASSWORD`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure port mapping to match your server
- [ ] Enable nginx reverse proxy (see below)
- [ ] Set up automatic backups of `quiz_data` volume
- [ ] Configure log rotation
- [ ] Test database persistence across restarts

### Nginx Reverse Proxy Configuration

See `deployment/nginx-nuclear-quiz.conf` for a production-ready reverse proxy setup.

```bash
# Copy nginx config to your server
scp deployment/nginx-nuclear-quiz.conf user@server:/etc/nginx/sites-available/quiz

# Enable the site
ssh user@server 'sudo ln -s /etc/nginx/sites-available/quiz /etc/nginx/sites-enabled/'

# Test and reload
ssh user@server 'sudo nginx -t && sudo systemctl reload nginx'
```

### Database Persistence

Your data persists in the Docker volume `nuclear_quiz_quiz_data`:

```bash
# View volume location
docker volume inspect nuclear_quiz_quiz_data

# Backup data
docker run --rm -v nuclear_quiz_quiz_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/quiz_backup_$(date +%Y%m%d).tar.gz -C /data .

# Restore from backup
docker run --rm -v nuclear_quiz_quiz_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/quiz_backup_20240115.tar.gz -C /data --strip-components=1
```

### Secrets in Docker

The `docker-compose.yml` reads environment variables from `.env`:

```yaml
environment:
  - SECRET_KEY=${SECRET_KEY:-change-this-secret-key}
  - ADMIN_PASSWORD=${ADMIN_PASSWORD:-changeme}
  - FLASK_ENV=${FLASK_ENV:-production}
```

✅ **Good**: Secrets are injected at runtime, not baked into the image
✅ **Safe**: `.env` is in `.gitignore` and never committed
❌ **Never do this**: `RUN export SECRET_KEY="hardcoded"` in Dockerfile

---

## 🔄 GitHub Actions CI/CD

### Automated Workflow

The `.github/workflows/test.yml` runs:
- Python syntax validation
- Dependency checks
- Database schema validation
- Security scanning (e.g., no hardcoded secrets)

```bash
# Test locally before pushing
python -m pytest tests/
```

### Deployment from GitHub

When you push to `main`:
1. ✅ Code is automatically tested
2. ✅ Security checks verify no secrets are present
3. ⚠️ Manual approval needed for production deployment
4. 🚀 Deploy to server: `git pull && docker compose up --build -d`

---

## 📋 Shared Server Setup (nuclear-motd.com)

Your app runs alongside `nuclear-motd-mobile` on the same server:

```
Server: nuclear-motd.com
├── quiz.nuclear-motd.com        (port 5001 → 5000 in container)
├── motd.nuclear-motd.com        (existing nuclear-motd app)
└── API endpoints at /api/*
```

### DNS Configuration

```dns
quiz.nuclear-motd.com    A  <your-server-ip>
```

### Nginx Upstream (Optional)

If running multiple services:

```nginx
upstream quiz_backend {
    server localhost:5001;
}

upstream motd_backend {
    server localhost:5002;
}

server {
    server_name quiz.nuclear-motd.com;
    location / {
        proxy_pass http://quiz_backend;
        # ... headers ...
    }
}
```

---

## 🔍 Monitoring & Troubleshooting

### Check Container Status

```bash
# View logs
docker compose logs -f quiz

# Watch container metrics
docker stats nuclear-quiz

# Shell into container
docker compose exec quiz sh
```

### Database Checks

```bash
# Verify database exists and is accessible
docker compose exec quiz sqlite3 /data/nuclear_quiz.db ".tables"

# Backup current state
docker compose exec quiz sqlite3 /data/nuclear_quiz.db ".dump" > backup.sql
```

### Performance Issues

```bash
# Check disk space (database growth)
docker exec nuclear-quiz du -sh /data/

# Check running processes inside container
docker compose exec quiz ps aux

# Monitor memory/CPU
docker stats --no-stream nuclear-quiz
```

---

## 🚀 Zero-Downtime Deployment

To deploy updates without downtime:

```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild image (without stopping current container)
docker compose build

# 3. Test new image (optional)
docker run --rm nuclear_quiz_quiz python app.py --version

# 4. Replace container gracefully
docker compose up -d --no-deps --build quiz

# 5. Verify new version
docker compose logs -f --tail=50 quiz
```

---

## 📝 Environment File Template

See `.env.example` for a template. Create `.env` locally with these values:

```bash
# CHANGE THESE IN PRODUCTION!
SECRET_KEY=your-super-secret-key-generated-with-secrets-module
ADMIN_PASSWORD=your-secure-admin-password
FLASK_ENV=production
PORT=5001
```

---

## 🆘 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "No SECRET_KEY provided" | Set `SECRET_KEY` in `.env` |
| "Permission denied" on `/data` | Docker user mismatch; rebuild image |
| Database locked | Close other connections; check `docker compose logs` |
| High memory usage | Clear `flask_session/` directory contents |
| Nginx 502 Bad Gateway | Verify container is running: `docker stack ps` |

---

## ✅ Verification Checklist

After deployment:

- [ ] App loads at `quiz.nuclear-motd.com`
- [ ] User registration works
- [ ] Quiz functionality works
- [ ] Admin panel protected by password
- [ ] Admin session expires after 2 hours
- [ ] Account management (change password, delete) works
- [ ] API endpoints return proper JSON (test with curl)
- [ ] Database persists after container restart
- [ ] Logs show no errors: `docker compose logs quiz`

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Nginx Reverse Proxy Guide](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

