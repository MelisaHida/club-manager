web: python manage.py collectstatic --noinput && gunicorn club_manager.wsgi --log-file -
release: python manage.py migrate --run-syncdb
