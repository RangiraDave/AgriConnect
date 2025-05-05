#!/usr/bin/env bash
# exit on error
set -o errexit

 # Ensure any half‑installed Django is removed
pip uninstall -y Django

# Install exactly what's in requirements, including Django==5.1.3
pip install --upgrade --force-reinstall -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Handle migrations
echo "Running migrations..."

# Remove all migration files except __init__.py
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete

# Create fresh migrations
python3 manage.py makemigrations core --noinput

# Apply migrations
python3 manage.py migrate --noinput

# Create superuser if it doesn't exist
python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END 