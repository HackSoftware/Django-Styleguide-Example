from .env_reader import env

CELERY_BROKER_URL = env('DJANGO_CELERY_BROKER_URL', default='amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERT_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3
