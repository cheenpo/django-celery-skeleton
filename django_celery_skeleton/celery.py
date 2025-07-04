import os
import sys
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
	sender.add_periodic_task(10.0, verify_workspace.s(), name='verify_workspace')

	#sender.add_periodic_task(1.0, test.s('periodic_task_1s'), name='every 1s')
	#sender.add_periodic_task(5.0, test.s('periodic_task_5s'), name='every 5s')

	## Executes every Monday morning at 7:30 a.m.
	#sender.add_periodic_task(
	#	crontab(hour=7, minute=30, day_of_week=1),
	#	test.s('Happy Mondays!'),
	#)

###
def validate_dir(dir):
	if not os.path.isdir(dir):
		print(f"INFO {dir} ... creating")
		os.mkdir(dir)

	if not os.path.isdir(dir):
		print(f"ERROR {dir} ... should exist")
		return False
	else:
		return True
#
def generate_log_file(taskname, contents):
	filename = f"{settings.SKELETON_LOGS}/{taskname}-{int(time.time())}.json"
	with open(filename, "w") as outfile:
		json.dump(contents, outfile, ensure_ascii=False)
	print(f"{filename} ... created")
#
def delete_expired_files(dir, expiration_days):
	current_time = time.time()
	files_deleted = []
	day = 86400 # seconds in a day
	for file in os.listdir(dir):
		file_full_path = f"{dir}/{file}"
		file_time = os.stat(file_full_path).st_mtime
		if(file_time < current_time - day*expiration_days):
			files_deleted.append(f"deleting ... {file_full_path}")
			os.remove(file_full_path)
	return files_deleted
###



@app.task
def test(arg):
	print(arg)

@app.task(name='verify_workspace')
def verify_workspace():
	results = {}
	results["validate_workspace"] = validate_dir(settings.SKELETON_WORKSPACE)
	results["validate_workspace_logs"] = validate_dir(settings.SKELETON_LOGS)
	results["delete_expired_workspace_logs"] = delete_expired_files(settings.SKELETON_LOGS, settings.SKELETON_LOGS_EXPIRE_DAYS)
	generate_log_file("verify_workspace", {"status": "success", "results": results})


##
app.send_task('verify_workspace')
