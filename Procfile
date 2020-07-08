release: python manage.py migrate
web: gunicorn config.wsgi:application
worker: REMAP_SIGTERM=SIGQUIT celery --without-gossip --without-mingle --without-heartbeat worker -A styleguide_example.tasks -l info
beat: REMAP_SIGTERM=SIGQUIT celery -A styleguide_example.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
