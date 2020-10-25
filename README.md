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

## Example List API

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
