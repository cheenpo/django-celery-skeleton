import os

from django.conf import settings
from django.http import JsonResponse
from django.views import View


class ShowLogs(View):
    def get(self, request):
        logs = []
        logfiles = os.listdir(settings.SKELETON_LOGS)
        for logfile in logfiles:
            logfile_s = logfile.split("-")
            logs.append({"filename": logfile, "taskname": logfile_s[0], "epoch": int(logfile_s[1].replace(".json", ""))})

        return JsonResponse({"status": "success", "logs": logs})
        #return JsonResponse({"status": "success"})
