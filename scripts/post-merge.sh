#!/bin/bash
set -e

pip install -r requirements.txt --quiet

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput
