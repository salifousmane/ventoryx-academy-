#!/bin/bash
set -e

cd /home/runner/workspace

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

exec python3 manage.py runserver 0.0.0.0:5000 --noreload
