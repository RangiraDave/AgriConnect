#!/usr/bin/env bash
# Exit on any error
set -o errexit

# Install exact dependencies
pip install -r requirements.txt

# Collect static assets
python3 manage.py collectstatic --no-input

# Run database migrations
echo "Running migrations..."
# Clean out old migration files (except __init__.py)
find core/migrations -type f -not -name "__init__.py" -delete

# Create new migrations for core app and apply all migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Remove contact column if it exists (PostgreSQL command)
if [[ -z "$DB_PASSWORD" || -z "$DB_HOST" || -z "$DB_USER" || -z "$DB_NAME" ]]; then
    echo "Error: One or more required database environment variables are not set."
    exit 1
fi

PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "ALTER TABLE core_product DROP COLUMN IF EXISTS contact;"

# Create default superuser if not exists
python3 manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END
