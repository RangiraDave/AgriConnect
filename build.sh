#!/usr/bin/env bash
# Exit on any error
set -o errexit

# Install exact dependencies
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Collect static assets
python3 manage.py collectstatic

# Run database migrations
echo "Running migrations..."
python3 manage.py makemigrations core
python3 manage.py migrate

# Import locations
python3 manage.py import_locations

# Create default superuser if not exists
python3 manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END
