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


def show_jobs(request, job=None):
    data = {"status": "in progress"}
    if job == 'all':
        job = ''
    base_uri = f"{request.scheme}://{request.get_host()}"
    jobs = []
    data["job_data"] = ""
    padding_top_counter = 0
    padding_top_counter_stop = False
    logfiles = os.listdir(settings.SKELETON_LOGS)
    for logfile in logfiles:
        match = False
        if not padding_top_counter_stop:
            padding_top_counter += 1
        if job and job in logfile:
            match = True
            padding_top_counter_stop = True
            try:
                with open(f"{settings.SKELETON_LOGS}/{logfile}", 'r') as file:
                    data["job_data"] += json.dumps(json.load(file), indent=4)
                    data["job_data"] += "\n"
            except FileNotFoundError:
                data["job_data"] += "<div class='alert alert-warning' role='alert'>job not found</div>"
            except json.JSONDecodeError:
                data["job_data"] += "<div class='alert alert-danger' role='alert'>invalid JSON format</div>"
        #
        logfile_s = logfile.split("-")
        seconds_since = int(time.time()) - int(logfile_s[1].replace(".json", ""))
        detail_uri = f"{base_uri}/jobs/{str(logfile).replace(".json", "")}"
        if job == '':
            match = False
        jobs.append({"job": logfile_s[0], "match": match, "uri": detail_uri, "time_since": seconds_in_pretty_time(seconds_since)})
    data["jobs"] = jobs
    data["job"] = job
    data["jobs_uri"] = f"{base_uri}/jobs/all"
    data["padding_top"] = 33 * padding_top_counter
    data["status"] = "success"
    #return JsonResponse(data)

    HTML_STRING = render_to_string("jobs.html", context=data)
    return HttpResponse(HTML_STRING)

#
