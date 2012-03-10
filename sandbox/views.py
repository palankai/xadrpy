from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    ctx = {}
    return render_to_response("sandbox/home.html", ctx, RequestContext(request))