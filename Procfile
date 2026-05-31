web: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput && gunicorn club_manager.wsgi --bind 0.0.0.0:$PORT --log-file -
