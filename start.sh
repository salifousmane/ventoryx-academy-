#!/bin/bash
set -e

cd /home/runner/workspace

python3 manage.py migrate --noinput 2>&1 | tail -5

python3 manage.py collectstatic --noinput 2>&1 | tail -3

exec python3 manage.py runserver 0.0.0.0:5000
