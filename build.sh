#!/usr/bin/env bash
# exit on error
set -o errexit

# Update pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Handle migrations
echo "Running migrations..."
# Drop all tables and recreate them
python3 manage.py dbshell << EOF
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
EOF

# Remove all migration files except __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create fresh migrations
python3 manage.py makemigrations --noinput

# Apply migrations
python3 manage.py migrate --noinput

# Create superuser if it doesn't exist
python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END 