#!/bin/sh
set -e

echo "Waiting for MindGlow Production RDS to be available..."
sleep 5

# 1. Run migrations 
# We add || true so it doesn't crash the container if the DB is momentarily busy
echo "Checking and running migrations..."
python manage.py migrate --noinput || echo "Migrations failed, continuing anyway..."

# 2. Collect static files
# We ignore errors here so that the server still starts even if S3 is not ready yet
echo "Collecting static files (Uploading to S3)..."
python manage.py collectstatic --noinput --clear || echo "Collectstatic failed (possibly S3 keys missing), continuing..."

# 3. Create superuser
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput || echo "Superuser exists"
fi

echo "Entrypoint script finished. Starting Gunicorn..."

# 4. Start Gunicorn (from CMD)
exec "$@"