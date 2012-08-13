from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    ctx = {
    }
    return render_to_response("home.html", ctx, RequestContext(request))
