import os
import time
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


def show_logs(request, taskname=None):
    print(taskname)
    #request.GET.get("q", None)
    logs = []
    logfiles = os.listdir(settings.SKELETON_LOGS)
    for logfile in logfiles:
        if taskname and taskname not in logfile:
            continue
        logfile_s = logfile.split("-")
        seconds_since = int(time.time()) - int(logfile_s[1].replace(".json", ""))
        logs.append({"filename": logfile, "taskname": logfile_s[0], "time_since": seconds_in_pretty_time(seconds_since)})
    data = {"status": "success", "logs": logs}
    #return JsonResponse(data)

    HTML_STRING = render_to_string("logs.html", context=data)
    return HttpResponse(HTML_STRING)
