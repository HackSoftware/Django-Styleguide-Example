# Django Styleguide Example

> 👀 **Need help with your Django project?** [HackSoft is here for you](https://www.hacksoft.io/solutions/django?utm_source=django-styleguide&utm_medium=web&utm_campaign=Django-Campaign). Reach out at `consulting@hacksoft.io`

**Table of contents:**

<!-- toc -->

- [How to ask a question or propose something?](#how-to-ask-a-question-or-propose-something)
- [What is this?](#what-is-this)
- [Structure](#structure)
- [General API Stuff](#general-api-stuff)
  * [CORS](#cors)
- [Authentication - JWT](#authentication---jwt)
  * [Settings](#settings)
  * [APIs](#apis)
  * [Requiring authentication](#requiring-authentication)
- [Authentication - Sessions](#authentication---sessions)
  * [DRF & Overriding `SessionAuthentication`](#drf--overriding-sessionauthentication)
  * [Cross origin](#cross-origin)
  * [APIs](#apis-1)
  * [`HTTP Only` / `SameSite`](#http-only--samesite)
  * [Reading list](#reading-list)
- [Example List API](#example-list-api)
- [File uploads](#file-uploads)
- [Helpful commands for local development without `docker compose`](#helpful-commands-for-local-development-without-docker-compose)
- [Helpful commands for local development with `docker compose`](#helpful-commands-for-local-development-with-docker-compose)
- [Deployment](#deployment)
  * [Heroku](#heroku)
  * [Render](#render)
  * [AWS ECS](#aws-ecs)
- [Linters and Code Formatters](#linters-and-code-formatters)

<!-- tocstop -->

---

## How to ask a question or propose something?

Few points to navigate yourself:

1. If you have an issue with something related to the Django Styleguide Example - **just open an issue. We will respond.**
1. If you have a general question or suggestion - **just open na issue. We will respond.**
1. Even if you have a question that you are not sure if it's related to the Django Styleguide - **just open an issue anyway. We will respond.**

That's about it ✨

## What is this?

Hello 👋

This projects serves as the following:

1. As an [example of our Django Styleguide](https://github.com/HackSoftware/Django-Styleguide), where people can explore actual code & not just snippets.
1. As a Django project, where we can test various things & concepts. A lot of the things you see here are being used as a foundation of our internal projects at [HackSoft](https://www.hacksoft.io/).
    - Usually, this is how something ends up as a section in the [Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)
1. As a place for all code examples from [our blog](https://www.hacksoft.io/blog).
    - Code snippets tend to decay & **we want most of our blog articles to be up to date.** That's why we place the code here, write tests for it & guarantee a longer shelf life of the examples.

If you want to learn more about the Django Styleguide, you can watch the videos below:

**Radoslav Georgiev's [Django structure for scale and longevity](https://www.youtube.com/watch?v=yG3ZdxBb1oo) for the philosophy behind the styleguide:**

[![Django structure for scale and longevity by Radoslav Georgiev](https://img.youtube.com/vi/yG3ZdxBb1oo/0.jpg)](https://www.youtube.com/watch?v=yG3ZdxBb1oo)

**Radoslav Georgiev & Ivaylo Bachvarov's [discussion on HackCast, around the Django Styleguide](https://www.youtube.com/watch?v=9VfRaPECbpY):**

[![HackCast S02E08 - Django Community & Django Styleguide](https://img.youtube.com/vi/9VfRaPECbpY/0.jpg)](https://www.youtube.com/watch?v=9VfRaPECbpY)

## Structure

The initial structure was inspired by [cookiecutter-django](https://github.com/pydanny/cookiecutter-django).

**The structure now is modified based on our work & production experience with Django.**

Few important things:

- Linux / Ubuntu is our primary OS and things are tested for that.
- It's dockerized for local development with `docker compose`.
- It uses Postgres as the primary database.
- It comes with [`whitenoise`](http://whitenoise.evans.io/en/stable/) setup, even for local development.
- It comes with [`mypy`](https://mypy.readthedocs.io/en/stable/) configured, using both <https://github.com/typeddjango/django-stubs> and <https://github.com/typeddjango/djangorestframework-stubs/>
  - Basic `mypy` configuration is located in [`setup.cfg`](setup.cfg)
  - `mypy` is ran as a build step in [`.github/workflows/django.yml`](.github/workflows/django.yml)
  - ⚠️ The provided configuration is quite minimal. **You should figure out your team needs & configure accordingly** - <https://mypy.readthedocs.io/en/stable/config_file.html>
- It comes with GitHub Actions support, [based on that article](https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/)
- It can be easily deployed to Heroku, Render or AWS ECS.
- It comes with an example list API, that uses [`django-filter`](https://django-filter.readthedocs.io/en/stable/) for filtering & pagination from DRF.
- It comes with setup for [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
- It comes with examples for writing tests with fakes & factories, based on the following articles - <https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories>, <https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories-advanced-usage>
- It comes with examples for how to add Google login, based on the following article - <https://www.hacksoft.io/blog/adding-google-login-to-your-existing-django-and-django-rest-framework-applications>

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
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])
```

## Authentication - JWT

The project is using <https://github.com/Styria-Digital/django-rest-framework-jwt> for having authentication via JWT capabilities.

### Settings

All JWT related settings are located in `config/settings/jwt.py`.

> ⚠️ We highly recommend reading the entire settings page from the project documentation - <https://styria-digital.github.io/django-rest-framework-jwt/#additional-settings> - to figure out your needs & the proper defaults for you!

The default settings also include the JWT token as a cookie.

The specific details about how the cookie is set, can be found here - <https://github.com/Styria-Digital/django-rest-framework-jwt/blob/master/src/rest_framework_jwt/compat.py#L43>

### APIs

The JWT related APIs are:

1. `/api/auth/jwt/login/`
1. `/api/auth/jwt/logout/`

The current implementation of the login API returns just the token:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InJhZG9yYWRvQGhhY2tzb2Z0LmlvIiwiaWF0IjoxNjQxMjIxMDMxLCJleHAiOjE2NDE4MjU4MzEsImp0aSI6ImIyNTEyNmY4LTM3ZDctNGI5NS04Y2M0LTkzZjI3MjE4ZGZkOSIsInVzZXJfaWQiOjJ9.TUoQQPSijO2O_3LN-Pny4wpQp-0rl4lpTs_ulkbxzO4"
}
```

This can be changed from `auth_jwt_response_payload_handler`.

### Requiring authentication

We follow this concept:

1. All APIs are public by default (no default authentication classes)
1. If you want a certain API to require authentication, you add the `ApiAuthMixin` to it.

## Authentication - Sessions

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

### APIs

1. `POST` to `/api/auth/session/login/` requires JSON body with `email` and `password`.
1. `GET` to `/api/auth/me/` returns the current user information, if the request is authenticated (has the corresponding `sessionid` cookie)
1. `GET` or `POST` to `/api/auth/logout/` will remove the `sessionid` cookie, effectively logging you out.

### `HTTP Only` / `SameSite`

The current implementation of `/api/auth/session/login` does 2 things:

1. Sets a `HTTP Only` cookie with the session id.
1. Returns the actual session id from the JSON payload.

The second thing is required, because Safari is not respecting the `SameSite = None` option for cookies.

More on the issue here - <https://www.chromium.org/updates/same-site/incompatible-clients>

### Reading list

Since cookies can be somewhat elusive, check the following urls:

1. <https://docs.djangoproject.com/en/3.1/ref/settings/#sessions> - It's a good idea to just read every description for `SESSION_*`
1. <https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies> - It's a good idea to read everything, several times.

## Example List API

You can find the `UserListApi` in [`styleguide_example/users/apis.py`](https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/users/apis.py#L12)

List API is located at:

<http://localhost:8000/api/users/>

The API can be filtered:

- <http://localhost:8000/api/users/?is_admin=True>
- <http://localhost:8000/api/users/?id=1>
- <http://localhost:8000/api/users/?email=radorado@hacksoft.io>

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

## File uploads

Following this article - <https://www.hacksoft.io/blog/direct-to-s3-file-upload-with-django> - there's a rich file-upload implementation in the Django Styleguide Example.

Everything is located in the `files` app.

Configuration wise, everything is located in [`config/settings/files_and_storages.py`](config/settings/files_and_storages.py)

Additionally, you can check the available options in [`.env.example`](.env.example)

Currently, the following is supported:

1. Standard local file upload.
1. Standard S3 file upload.
1. Using CloudFront as CDN.
1. The so-called "direct" upload that can work both locally and with S3 (for more context, [check the article](https://www.hacksoft.io/blog/direct-to-s3-file-upload-with-django))

Feel free to use this as the basis of your file upload needs.

## Helpful commands for local development without `docker compose`

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
celery -A styleguide_example.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
```

To start Celery Beat:

```
celery -A styleguide_example.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Helpful commands for local development with `docker compose`

To build and run everything

```
docker compose up
```

To run migrations

```
docker compose run django python manage.py migrate
```

To shell

```
docker compose run django python manage.py shell
```

## Deployment

This project is ready to be deployed either on **Heroku** **Render** or **AWS ECS**.

### Heroku

Deploying a Python / Django application on Heroku is quite straighforward & this project is ready to be deployed.

To get an overview of how Heroku deployment works, we recommend reading this first - <https://devcenter.heroku.com/articles/deploying-python>

**Files related to Heroku deployment:**

1. `Procfile`
   - Comes with default `web`, `worker` and `beat` processes.
   - Additionally, there's a `release` phase to run migrations safely, before releasing the new build.
1. `runtime.txt`
   - Simply specifies the Python version to be used.
1. `requirements.txt`
   - Heroku requires a root-level `requirements.txt`, so we've added that.

**Additionally, you need to specify at least the following settings:**

1. `DJANGO_SETTINGS_MODULE`, usually to `config.django.production`
1. `SECRET_KEY` to something secret. [Check here for ideas](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django).
1. `ALLOWED_HOSTS`, usually to the default heroku domain (for example - `hacksoft-styleguide-example.herokuapp.com`)

On top of that, we've added `gunicorn.conf.py` with some example settings.

**We recommend the following materials, to figure out `gunicorn` defaults and configuration:**

1. <https://devcenter.heroku.com/articles/python-gunicorn>
1. <https://adamj.eu/tech/2019/09/19/working-around-memory-leaks-in-your-django-app/>
1. <https://adamj.eu/tech/2021/12/29/set-up-a-gunicorn-configuration-file-and-test-it/>
1. Worker settings - <https://docs.gunicorn.org/(en/latest/settings.html#worker-processes>
1. A brief description of the architecture of Gunicorn - <https://docs.gunicorn.org/en/latest/design.html>

### Render

To get an overview of how Render deployment works, we recommend reading this first - <https://render.com/docs/deploy-django>

There's a current deployment that can be found here - <https://django-styleguide.hacksoft.io/>

**Files related to Heroku deployment:**

1. `render.yaml`
    - Describes the setup. Also known as [Render Blueprint](https://render.com/docs/blueprint-spec)
1. `docker/*_entrypoint.sh`
    - Entrypoint for every different process type.
1. `docker/production.Dockerfile`
    - Dockerfile for production build.
1. `requirements.txt`
    - Heroku requires a root-level `requirements.txt`, so we've added that.

### AWS ECS

_Coming soon_

## Linters and Code Formatters

In all our Django projects we use:

- [flake8](https://flake8.pycqa.org/en/latest/) - a linter that ensures we follow the PEP8 conventions.
- [black](https://github.com/psf/black) - a code formatter that ensures we have the same code style everywhere.
- [isort](https://github.com/PyCQA/isort) - a code formatter that ensures we have the same import style everywhere.
- [pre-commit](https://pre-commit.com/) - a tool that triggers the linters before each commit.

To make sure all of the above tools work in symbiosis, you'd need to add some configuration:

1. Add `.pre-commit-config.yaml` file to the root of your project. There you can add the instructions for `pre-commit`
2. Add `pyproject.toml` file to the root of your project. There you can add the `black` config. **NOTE:** `black` [does not respect any other config files.](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
3. Add the following to `setup.cfg` for the `isort` config:

```
[isort]
profile = black
```

This will tell `isort` to follow the `black` guidelines.

```
[isort]
filter_files = true
skip_glob = */migrations/*
```

This will tell `pre-commit` to respect the `isort` config.

4. You can add a custom `flake8` configuration to `setup.cfg` as well. We usually have the following config in all our projects:

```
[flake8]
max-line-length = 120
extend-ignore = E203
exclude =
    .git,
    __pycache__,
    */migrations/*
```

5. Make sure the linters are run against each PR on your CI. This is the config you need if you use GH actions:

```
build:
  runs-on: ubuntu-latest
  steps:
    - name: Run isort
      uses: isort/isort-action@master
    - name: Run black
      uses: psf/black@stable
    - name: Run flake8
      run: flake8
```

6. Last but not least, we highly recommend you to setup you editor to run `black` and `isort` every time you save a new Python file.

In order to test if your local setup is up to date, you can either:

1. Try making a commit, to see if `pre-commit` is going to be triggered.
1. Or run `black --check .` and `isort --check .` in the project root directory.
