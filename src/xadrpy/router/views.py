from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,\
    HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
    
def static(request, route):
    return HttpResponse(route.path, route.mimetype or '')

def template(request, route):
    ctx = route.context
    return render_to_response(route.template, ctx, RequestContext(request), mimetype=route.mimetype)

def redirect(request, route):
    if route.permanent:
        return HttpResponsePermanentRedirect(route.url)
    return HttpResponseRedirect(route.url)
