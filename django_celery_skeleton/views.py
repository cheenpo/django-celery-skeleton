import os
import time
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


##
def seconds_in_pretty_time(seconds):
    sign_string = "-" if seconds < 0 else ""
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return_string = sign_string
    if days > 0:
        return_string += f"{days}d"
    if hours > 0:
        return_string += f"{hours}h"
    if minutes > 0:
        return_string += f"{minutes}m"
    if seconds > 0:
        return_string += f"{seconds}s"
    return return_string
##


def show_jobs(request, taskname=None):
    data = {"status": "in progress"}
    jobs = []
    logfiles = os.listdir(settings.SKELETON_LOGS)
    for logfile in logfiles:
        if taskname and taskname not in logfile:
            continue
        logfile_s = logfile.split("-")
        seconds_since = int(time.time()) - int(logfile_s[1].replace(".json", ""))
        base_uri = f"{request.scheme}://{request.get_host()}"
        detail_uri = f"{base_uri}/job/{str(logfile).replace(".json", "")}"
        jobs.append({"filename": str(logfile), "taskname": logfile_s[0], "uri": detail_uri, "time_since": seconds_in_pretty_time(seconds_since)})
    data["status"] = "success"
    data["jobs"] = jobs
    data["taskname"] = taskname
    data["jobs_uri"] = f"{base_uri}/jobs"
    #return JsonResponse(data)

    HTML_STRING = render_to_string("jobs.html", context=data)
    return HttpResponse(HTML_STRING)

#
def show_job(request, job=None):
    data = {"status": "in progress", "job": job}
    logfile = f"{settings.SKELETON_LOGS}/{job}.json"
    base_uri = f"{request.scheme}://{request.get_host()}"
    #
    logfile_s = job.split("-")
    seconds_since = int(time.time()) - int(logfile_s[1])
    data["taskname"] = logfile_s[0]
    data["job_time_since"] = seconds_in_pretty_time(seconds_since)
    job_data = {}
    try:
        with open(logfile, 'r') as file:
            data["job_data"] = json.dumps(json.load(file), indent=4)
            data["status"] = "success"
    except FileNotFoundError:
        data["status"] = "failed"
        data["fail_message"] = "job not found"
    except json.JSONDecodeError:
        data["status"] = "failed"
        data["fail_message"] = "Invalid JSON format"
    #
    data["jobs_uri"] = f"{base_uri}/jobs"
    HTML_STRING = render_to_string("job.html", context=data)
    return HttpResponse(HTML_STRING)
