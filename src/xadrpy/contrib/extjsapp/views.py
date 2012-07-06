from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

def extjsapp(request, application, appcss=None, template="xadrpy/extjsapp/base.html"):
    ctx = {
        'application': None,
        'appjs': application,
        'appcss': appcss,
        'debug': settings.DEBUG,
    }
    return render_to_response(template, ctx, RequestContext(request))