.DEFAULT_GOAL := install
.PHONY: default
default: install ;

install:
	poetry install

web:
	poetry run python manage.py runserver

worker:
	poetry run celery -A django_celery_skeleton worker

beat:
	poetry run celery -A django_celery_skeleton beat
