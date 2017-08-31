from django.http import JsonResponse


def handler404(request):
    response = JsonResponse({'detail':'Not found'})
    response.status_code = 404
    return response


def handler500(request):
    response = JsonResponse({'detail': 'Internal Server Error'})
    response.status_code = 500
    return response
