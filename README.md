## helpful commands
 - `poetry run celery -A django_celery_skeleton beat`
    - starts the heartbeat for scheduled jobs going
 - `poetry run celery -A django_celery_skeleton worker`
    - starts the actual worker
 - `poetry run python manage.py runserver`
    - starts the server

## next steps
 - set up views to dynamically update with new job logs
 - set up view to see details of job

## eventually
 - wrap it all up in docker-compose
