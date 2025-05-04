#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate

# Create superuser if it doesn't exist
python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END 