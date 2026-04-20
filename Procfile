release: python manage.py collectcss --noinput
web: gunicorn hireme.wsgi:application --log-file - --log-level debug
