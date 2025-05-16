from django.http import JsonResponse
from .tasks import my_task

def my_view(request):
    result = my_task.delay(4, 5) # Send the task to the queue
    return JsonResponse({'task_id': result.id})