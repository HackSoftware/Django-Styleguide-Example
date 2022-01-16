echo "--> Starting celery process"
celery -A styleguide_example.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler