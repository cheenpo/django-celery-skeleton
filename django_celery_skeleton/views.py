import os

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.template.loader import render_to_string


class ShowLogs(View):
    def get(self, request):
        logs = []
        logfiles = os.listdir(settings.SKELETON_LOGS)
        for logfile in logfiles:
            logfile_s = logfile.split("-")
            logs.append({"filename": logfile, "taskname": logfile_s[0], "epoch": int(logfile_s[1].replace(".json", ""))})
        data = {"status": "success", "logs": logs}
        #return JsonResponse(data)

        HTML_STRING = render_to_string("logs.html", context=data)
        return HttpResponse(HTML_STRING)
