#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py makemigrations
python manage.py migrate
python manage.py runscript load_chroma

uwsgi --socket :8000 --workers 4 --master --enable-threads -b 32768 --module app.wsgi
