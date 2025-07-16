#!/bin/sh

set -e

echo "Warte auf PostgreSQL auf $DB_HOST:$DB_PORT..."

# -q für "quiet" (keine Ausgabe außer Fehlern)
# Die Schleife läuft, solange pg_isready *nicht* erfolgreich ist (Exit-Code != 0)
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL ist nicht erreichbar - schlafe 1 Sekunde"
  sleep 1
done

echo "PostgreSQL ist bereit - fahre fort..."

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Deine originalen Befehle (ohne wait_for_db)
python manage.py collectstatic --noinput

# First run initial Django migrations
python manage.py migrate

# Then create app-specific migrations
python manage.py makemigrations authentication
python manage.py makemigrations videos  
python manage.py makemigrations utils

# Apply the new migrations
python manage.py migrate

# Create a superuser using environment variables
# (Dein Superuser-Erstellungs-Code bleibt gleich)
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    # Korrekter Aufruf: username hier übergeben
    user = User.objects.create_superuser(username=username, email=email, password=password)
    # Set email verification
    user.is_email_verified = True
    user.save()
    print(f"Verification email would be sent to {email} with token: (auto-verified)")
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
    # Verify existing admin user
    user = User.objects.get(username=username)
    user.is_email_verified = True
    user.save()
    print(f"Admin user '{username}' verified.")
EOF

python manage.py rqworker default &

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
