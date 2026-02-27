FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser app.py helpers.py api.py init_db.py schema.sql ./
COPY --chown=appuser:appuser static/ static/
COPY --chown=appuser:appuser templates/ templates/

# Copy seed database (full question set baked into image)
COPY --chown=appuser:appuser nuclear_quiz.db /app/nuclear_quiz.db.seed

# Create data directory for DB and sessions
RUN mkdir -p /data/flask_session && chown -R appuser:appuser /data

# Switch to non-root user
USER appuser

# Expose Flask/gunicorn port
EXPOSE 5000

# Health check (python only — curl not available in slim image)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()" || exit 1

# Seed DB from image if volume is empty, then start gunicorn
CMD ["sh", "-c", "[ -f /data/nuclear_quiz.db ] || cp /app/nuclear_quiz.db.seed /data/nuclear_quiz.db && gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 --worker-tmp-dir /dev/shm --access-logfile - --error-logfile - app:app"]
