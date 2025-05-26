## helpful commands
 - `poetry run celery -A django_celery_skeleton beat`
    - starts the heartbeat for scheduled jobs going
 - `poetry run celery -A django_celery_skeleton worker`
    - starts the actual worker
 - `poetry run python manage.py runserver`
    - starts the server

## next steps
 - docker-compose

## nice to have
 - set up view to dynamically update with new job logs
