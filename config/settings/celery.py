from .env_reader import env

CELERY_BROKER_URL = env('DJANGO_CELERY_BROKER_URL', default='amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = 'django-db'
