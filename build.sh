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
if [[ -z "$EXTERNAL_DATABASE_URL" ]]; then
    echo "Error: EXTERNAL_DATABASE_URL environment variable is not set."
    exit 1
fi

# Extract database connection details from DATABASE_URL
DB_HOST=$(echo $EXTERNAL_DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $EXTERNAL_DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
DB_NAME=$(echo $EXTERNAL_DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
DB_USER=$(echo $EXTERNAL_DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
DB_PASSWORD=$(echo $EXTERNAL_DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')

# Remove contact column using extracted connection details
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "ALTER TABLE core_product DROP COLUMN IF EXISTS contact;"

# Create default superuser if not exists
python3 manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END
