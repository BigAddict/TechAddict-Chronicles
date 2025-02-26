#!/bin/bash

# Activate virtual environment
source /home/ubuntu/django-blog/.venv/bin/activate
export PYTHON=$(which python)

# Run Django management commands
$PYTHON manage.py makemigrations
$PYTHON manage.py migrate
$PYTHON manage.py collectstatic --noinput

# Start Gunicorn (Modify as needed)
exec gunicorn --access-logfile - --error-logfile - --workers 3 --bind unix:/run/gunicorn.sock django_blog.wsgi:application