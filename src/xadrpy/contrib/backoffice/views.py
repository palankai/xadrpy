from xadrpy.contrib.backoffice.forms import LoginForm
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from xadrpy.core.access.models import Consumer,Access,Token
from django.core.urlresolvers import reverse
import conf
from django.utils.safestring import mark_safe
from xadrpy.utils.jsonlib import JSONEncoder
from django.conf import settings
from django.template.loader import render_to_string
from xadrpy.contrib.backoffice.generic import store_manager, model_manager


def extlogin(request):
    config = {
        'title': conf.TITLE,
        'api_path': reverse("APIBASE"),
        'redirect_uri': reverse("xadrpy.contrib.backoffice.views.backoffice"),
         
    }
    ctx = {
        'config': mark_safe(JSONEncoder().encode(config)),
        'title': conf.TITLE,
        'description': conf.DESCRIPTION,
    }
    return render_to_response("xadrpy/backoffice/extlogin.html", ctx, RequestContext(request))

def login(request):
    backoffice_client = Consumer.objects.get_static("backoffice")
    if request.user.is_authenticated():
        auth.logout(request)
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            Access.objects.get_or_create(client=backoffice_client, user=user)
            token = Token(client=backoffice_client, user=user)
            token.generate_token()
            request.session['backoffice-token'] = token.token
            return HttpResponseRedirect(reverse("xadrpy.contrib.backoffice.views.backoffice"))
    else:
        form = LoginForm()
    ctx = {
        'form': form,
        'client': backoffice_client
    }
    return render_to_response("xadrpy/backoffice/login.html", ctx, RequestContext(request))
            

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect(reverse("xadrpy.contrib.backoffice.views.backoffice"))

def backoffice(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('xadrpy.contrib.backoffice.views.extlogin'))
    config = {
        'namespaces': conf.NAMESPACES,
        'controllers': conf.CONTROLLERS,
        'debug': settings.DEBUG,
        'api_path': reverse("APIBASE"),
        'title': conf.TITLE,
        'logout_url': reverse('xadrpy.contrib.backoffice.views.logout'),
        'icons': settings.STATIC_URL+"xadrpy/backoffice/css/icons/",
        'username': request.user.username,
        'user_display': "%s %s (%s)" % (request.user.last_name,request.user.first_name,request.user.username) if request.user.first_name and request.user.last_name else request.user.username,
        'user_id': request.user.id
    }
    ctx = {
        'access_token': request.session.get("backoffice-token"),
        'config': mark_safe(JSONEncoder(indent=4).encode(config)),
        'title': conf.TITLE,
        'description': conf.DESCRIPTION,
    }
    return render_to_response("xadrpy/backoffice/backoffice.html", ctx, RequestContext(request))

def generic(request):
    content = []
    
    content.extend([obj.render(request) for obj in model_manager.get_items()])
    content.extend([obj.render(request) for obj in store_manager.get_items()])
    
    return HttpResponse("\n".join(content), mimetype="text/javascript")
