from django.http import HttpResponseNotFound


def favicon(request):
    return HttpResponseNotFound()
