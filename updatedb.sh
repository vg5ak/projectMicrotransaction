#!/bin/bash

# echo "hello world"

python manage.py makemigrations

python manage.py migrate

python manage.py sqlflush

python manage.py loaddata db.json