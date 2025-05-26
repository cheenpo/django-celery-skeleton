## helpful commands
 - `make` or `poetry install`
    - installs things
 - `make web` or `poetry run python manage.py runserver`
    - starts the web server
 - `make worker` or `poetry run celery -A django_celery_skeleton worker`
    - starts the worker
 - `make beat` or `poetry run celery -A django_celery_skeleton beat`
    - gets the scheduled jobs going

## next steps

## nice to have
 - set up view to dynamically update with new job logs
 - docker-compose
