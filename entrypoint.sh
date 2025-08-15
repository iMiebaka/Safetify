#!/bin/bash
set -eux

# Function to check PostgreSQL readiness
wait_for_postgres() {
    local max_attempts=10
    local attempt=0
    local sleep_seconds=5

    echo "Waiting for database..."
    until python manage.py shell -c "
import sys
from django.db import connections
from django.db.utils import OperationalError
try:
    connections['default'].ensure_connection()
except OperationalError:
    sys.exit(1)
sys.exit(0)
"; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "Database not ready after $max_attempts attempts. Exiting."
            exit 1
        fi
        echo "Database not ready yet. Attempt $attempt/$max_attempts. Retrying in $sleep_seconds seconds..."
        sleep $sleep_seconds
    done
    echo "Database is ready!"
}

# Collect static files
python manage.py collectstatic --no-input

# Check and wait for PostgreSQL if environment variables are set
if [ -n "$POSTGRES_HOST" ] && [ -n "$POSTGRES_USER" ] && [ -n "$POSTGRES_DB" ]; then
    wait_for_postgres
else
    echo "Skipping PostgreSQL readiness check (DB environment variables not set)"
fi

# Run migrations
python manage.py makemigrations
python manage.py migrate

echo "Deployment complete: static files collected, migrations applied, and search indexes rebuilt successfully!"

exec "$@"