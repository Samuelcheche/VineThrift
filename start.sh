#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
python scripts/bootstrap_admin.py
python manage.py collectstatic --noinput

exec gunicorn Vinethrift.wsgi:application --bind 0.0.0.0:${PORT:-10000}
