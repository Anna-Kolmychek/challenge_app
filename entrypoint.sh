#!/bin/env
echo "Making migrations..."
python manage.py makemigrations
echo "Running migrations..."
python manage.py migrate

echo "Importing test users..."
python manage.py create_users
echo "Importing test challenges and progress..."
python manage.py create_challenges


echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting Celery worker..."
celery -A config worker --loglevel=info &

echo "Starting Celery Beat..."
celery -A config beat --loglevel=info &

echo "Starting gunicorn..."
gunicorn --bind 0.0.0.0:9000 --workers 3 config.wsgi:application 0
exec "$@"
