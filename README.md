# project-1-38

1. How to use the Code

When pulling from github clear the database with
    git pull
    chmod +x ./updatedb.sh
    ./updatedb.sh

When pushing to github
    chmod +x ./exportdb.sh
    ./exportdb.sh
    git add .
    git commit -m "ENTER YOUR MESSAGE"
    git push


When running lazily (makes migrations, runserver for you):
Will run python manage.py makemigrations, migrate, and runserver in one command

    ./lazy.sh

Install the requirements
    pip install -r requirements.txt

2. The different features of the app
This project was made by a group of University of Virginia students.
