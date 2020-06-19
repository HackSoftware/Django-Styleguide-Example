#!/bin/bash

E_NO_POSTGRES_USERNAME=60

POSTGRES_USERNAME="$1"
DATABASE_NAME="styleguide_example"

if [[ -z "$POSTGRES_USERNAME" ]]
then
  echo "Call `basename $0` with your postgres user as the first argument."
  exit "$E_NO_POSTGRES_USERNAME"
fi

dropdb --if-exists "$DATABASE_NAME"

sudo -u postgres createdb -O "$POSTGRES_USERNAME" "$DATABASE_NAME"

python manage.py migrate
