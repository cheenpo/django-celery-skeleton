from django.http import JsonResponse

def view1(request):
    return JsonResponse({"status": "success"})
