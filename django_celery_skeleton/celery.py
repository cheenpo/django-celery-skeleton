import os
import json
import time
from celery import Celery
from celery.schedules import crontab

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_celery_skeleton.settings")
app = Celery("django_celery_skeleton")
app.config_from_object("django.conf:settings", namespace="SKELETON")

#app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
	sender.add_periodic_task(2.0, verify_workspace.s(), name='verify_workspace')
	#sender.add_periodic_task(1.0, test.s('periodic_task_1s'), name='every 1s')
	#sender.add_periodic_task(5.0, test.s('periodic_task_5s'), name='every 5s')

	## Executes every Monday morning at 7:30 a.m.
	#sender.add_periodic_task(
	#	crontab(hour=7, minute=30, day_of_week=1),
	#	test.s('Happy Mondays!'),
	#)

###
def validate_dir(dir):
	if os.path.isdir(dir):
		print(f"DEBUG {dir} ... already exists")
	else:
		print(f"INFO {dir} ... creating")
		os.mkdir(dir)

	if not os.path.isdir(dir):
		print(f"ERROR {dir} ... should exist")
		return False
	else:
		return True

###



@app.task
def test(arg):
	print(arg)

@app.task
def verify_workspace():
	validate_dir(settings.SKELETON_WORKSPACE)

@app.task
def generate_file(taskname, contents):
	with open(f"{taskname}-{time.time()}.json", "w") as outfile:
		outfile.write(contents)
