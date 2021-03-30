# Styleguide-Example

This project serves as an [example of our styleguide](https://github.com/HackSoftware/Django-Styleguide)

The structure is inspired by [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) and modified based on our experience with Django.

Few important things:

* Linux / Ubuntu is our primary OS and things are tested for that. It will mostly not work on Mac & certainly not work on Windows.
* It uses Postgres as primary database.
* It comes with GitHub Actions support, [based on that article](https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/)
* It comes with [`whitenoise`](http://whitenoise.evans.io/en/stable/) setup.
* It can be easily deployed to Heroku.
* It comes with an example list API, that uses [`django-filter`](https://django-filter.readthedocs.io/en/stable/) for filtering & pagination from DRF.

## General API Stuff

### CORS

The project is running [`django-cors-headers`](https://github.com/adamchainz/django-cors-headers) with the following general configuration:

```python
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
```

For `production.py`, we have the following:

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST', default=[])
```

### DRF

We have removed the default authentication classes, since they were causing trouble.

## Authentication - General

This project is using the already existing [**cookie-based session authentication**](https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in) in Django:

1. On successful authentication, Django returns the `sessionid` cookie:

```
sessionid=5yic8rov868prmfoin2vhtg4vx35h71p; expires=Tue, 13 Apr 2021 11:17:58 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax
```

2. When making calls from the frontend, don't forget to **include credentials**. For example, when using `axios`:

```javascript
axios.get(url, { withCredentials: true });
axios.post(url, data, { withCredentials: true });
```

3. For convenience, `CSRF_USE_SESSIONS` is set to `True` 

4. Check `config/settings/sessions.py` for all configuration that's related to sessions.

### DRF & Overriding `SessionAuthentication`

Since the default implementation of `SessionAuthentication` enforces CSRF check, which is not the desired behavior for our APIs, we've done the following:

```python
from rest_framework.authentication import SessionAuthentication


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """
    def enforce_csrf(self, request):
        return
```

Which is then used to construct an `ApiAuthMixin`, which marks an API that requires authentication:

```python
from rest_framework.permissions import IsAuthenticated


class ApiAuthMixin:
    authentication_classes = (CsrfExemptedSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
```

**By default, all APIs are public, unless you add the `ApiAuthMixin`**

### Cross origin

We have the following general cases:

1. The current configuration works out of the box for `localhost` development.
1. If the backend is located on `*.domain.com` and the frontend is located on `*.domain.com`, the configuration is going to work out of the box.
1. If the backend is located on `somedomain.com` and the frontend is located on `anotherdomain.com`, then you'll need to set `SESSION_COOKIE_SAMESITE = 'None'` and `SESSION_COOKIE_SECURE = True`

### Reading list

Since cookies can be somewhat elusive, check the following urls:

1. <https://docs.djangoproject.com/en/3.1/ref/settings/#sessions> - It's a good idea to just read every description for `SESSION_*`
1. <https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies> - It's a good idea to read everything, several times.

## Authentication APIs

1. `POST` <http://localhost:8000/api/auth/login/> requires JSON body with `email` and `password`.
1. `GET` <http://localhost:8000/api/auth/me/> returns the current user information, if the request is authenticated (has the corresponding `sessionid` cookie)
1. `GET` or `POST` <http://localhost:8000/api/auth/logout/> will remove the `sessionid` cookie, effectively logging you out.

## Example List API

You can find the `UserListApi` in [`styleguide_example/users/apis.py`](https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/users/apis.py#L12)

List API is located at:

<http://localhost:8000/api/users/>

The API can be filtered:

* <http://localhost:8000/api/users/?is_admin=True>
* <http://localhost:8000/api/users/?id=1>
* <http://localhost:8000/api/users/?email=radorado@hacksoft.io>

Example data structure:

```
{
    "limit": 1,
    "offset": 0,
    "count": 4,
    "next": "http://localhost:8000/api/users/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "radorado@hacksoft.io",
            "is_admin": false
        }
    ]
}
```

## Helpful commands

To create Postgres database:

```
sudo -u postgres createdb -O your_postgres_user_here database_name_here
```

If you want to recreate your database, you can use the bootstrap script:

```
./scripts/bootstrap.sh your_postgres_user_here
```

To start Celery:

```
celery --without-gossip --without-mingle --without-heartbeat worker -A styleguide_example.tasks -l info
```

To start Celery Beat:

```
celery -A styleguide_example.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Heroku

The project is ready to be deployed on Heroku. There's a current deployment that can be found - <https://hacksoft-styleguide-example.herokuapp.com/>
