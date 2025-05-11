#!/usr/bin/env bash
# Exit on any error
set -o errexit

# Install exact dependencies
pip install -r requirements.txt

# Collect static assets
python3 manage.py collectstatic --no-input

# Run database migrations
echo "Running migrations..."

# First, ensure core app is installed
python3 manage.py makemigrations core
python3 manage.py migrate

# Remove contact column if it exists (PostgreSQL command)
# psql -c "ALTER TABLE core_product DROP COLUMN IF EXISTS contact;"

# Create default superuser if not exists
python3 manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END
