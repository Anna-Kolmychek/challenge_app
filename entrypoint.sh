#!/bin/env
echo "Making migrations..."
python manage.py makemigrations
echo "Running migrations..."
python manage.py migrate

echo "Importing test users..."
python manage.py create_users
echo "Importing test challenges..."
python manage.py create_challenges
echo "Importing test progress..."
python manage.py create_progress


echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
gunicorn --bind 0.0.0.0:9000 --workers 3 config.wsgi:application 0
exec "$@"
