#!/bin/bash
set -e

echo "🔍 Checking environment variables..."
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"

echo "⏳ Waiting for PostgreSQL on $DB_HOST:$DB_PORT..."

# Enhanced PostgreSQL readiness check
wait_for_postgres() {
    local max_attempts=60
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -q; then
            echo "✅ PostgreSQL is ready!"
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts - PostgreSQL not ready, waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ PostgreSQL failed to become ready after $max_attempts attempts"
    exit 1
}

wait_for_postgres

# Test actual database connection
echo "🔗 Testing database connection..."
python manage.py check --database default

# Create logs directory
mkdir -p /app/logs

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Only apply migrations (creation handled by setup.py)
echo "⚡ Applying migrations..."
python manage.py migrate

# Create superuser
echo "👤 Setting up admin user..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@test.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    user = User.objects.create_superuser(username=username, email=email, password=password)
    user.is_email_verified = True
    user.save()
    print(f"✅ Superuser '{username}' created and verified.")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
    user = User.objects.get(username=username)
    user.is_email_verified = True
    user.save()
    print(f"✅ Admin user '{username}' verified.")
EOF

echo "🚀 Starting application services..."

# Start RQ worker in background
python manage.py rqworker default &

# Start Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 3
