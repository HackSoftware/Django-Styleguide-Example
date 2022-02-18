# If you are not having memory issues, just delete this.
# This is primarily to prevent memory leaks
# Based on https://devcenter.heroku.com/articles/python-gunicorn
# Based on https://adamj.eu/tech/2019/09/19/working-around-memory-leaks-in-your-django-app/
# https://docs.gunicorn.org/en/latest/settings.html#max-requests
# https://docs.gunicorn.org/en/latest/settings.html#max-requests-jitter
max_requests = 1200
max_requests_jitter = 100
