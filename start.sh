#!/bin/bash
#while ! nc -z db 3306; do
#    echo "Waiting for the MySQL Server"
#    sleep 3
#done
#sleep 3
python3 manage.py collectstatic --noinput&&
python3 manage.py makemigrations&&
python3 manage.py migrate&&
uwsgi --ini /app/uwsgi.ini&&
tail -f /dev/null
exec "$@"