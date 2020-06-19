# Styleguide-Example

This project serves as an [example of our styleguide](https://github.com/HackSoftware/Django-Styleguide)

The structure is inspired by [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) and modified based on our experience with Django.

Few important things:

* Linux / Ubuntu is our primary OS and things are tested for that. It will mostly not work on Mac & certainly not work on Windows.
* It uses Postgres as primary database.
* It comes with GitHub Actions support, [based on that article](https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/)

## Helpful commands

To create Postgres database:

```
sudo -u postgres createdb -O your_postgres_user_here database_name_here
```

If you want to recreate your database, you can use the bootstrap script:

```
./scripts/bootstrap.sh your_postgres_user_here
```
