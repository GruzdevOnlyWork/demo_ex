#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py clear_all_data --yes --keep-tests
python manage.py load_variant2
python manage.py load_general_modules
