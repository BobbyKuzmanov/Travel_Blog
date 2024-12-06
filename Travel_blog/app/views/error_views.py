from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseNotFound


def handler404(request, exception=None):
    template = loader.get_template('404-error.html')
    context = {
        'request': request,
        'exception': exception,
    }
    return HttpResponseNotFound(template.render(context, request))
