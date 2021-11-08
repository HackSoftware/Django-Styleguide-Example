echo "--> Starting web app"
gunicorn config.wsgi:application -b 0.0.0.0:80
