# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=minimalist_marketplace.settings \
    DEBUG=1 \
    SECRET_KEY=docker-dev-secret-key-change-in-production \
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,* \
    DATABASE_URL=sqlite:///db.sqlite3 \
    STATIC_URL=/static/ \
    MEDIA_URL=/media/ \
    STATIC_ROOT=/app/static \
    MEDIA_ROOT=/app/media

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
        gettext \
        netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==21.2.0

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p media static logs

# Run migrations and collect static files during build
RUN python manage.py migrate --noinput || echo "Migration skipped (database may not be ready)" \
    && python manage.py collectstatic --noinput --clear || echo "Static collection skipped"

# Create a simple startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=== Starting Minimalist Marketplace ==="\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput || echo "Migration failed, continuing..."\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear || echo "Static collection failed, continuing..."\n\
echo "Compiling messages..."\n\
python manage.py compilemessages --ignore=venv || echo "Message compilation skipped"\n\
echo "Creating cache table..."\n\
python manage.py createcachetable || echo "Cache table creation skipped"\n\
echo "Starting server on 0.0.0.0:8000..."\n\
echo "=== Server Ready ==="\n\
exec "$@"' > /app/startup.sh && chmod +x /app/startup.sh

# Expose port
EXPOSE 8000

# Use startup script
ENTRYPOINT ["/app/startup.sh"]

# Run gunicorn
CMD ["gunicorn", "minimalist_marketplace.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]