from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from xadrpy.core.access.base import rights
import logging
import conf
import base
from xadrpy.utils.jsonlib import JSONEncoder
from xadrpy.core.api.exceptions import ServiceException

logger = logging.getLogger("xadrpy.core.api.views")

from decorators import APIInterface

api = APIInterface(r"api/")


def home(request):
    pass

def serve(request, name, namespace=None):
    try:
        service, options, registry = conf.HTTP_SERVICES[(namespace, name)]
    except KeyError, e:
        logger.error("Service '%s/%s' not found: ", namespace, name)
        raise Http404("Service '%s/%s' not found" % (namespace, name))
    status = 200
    kwargs = {
        'request': request
    }

    for arg in options['args']:
        src = request.REQUEST
        if arg.startswith("GET:"): arg = arg[4:]; src = request.GET
        elif arg.startswith("POST:"): arg = arg[5:]; src = request.POST
        elif arg.startswith("FILE:"): arg = arg[5:]; src = request.FILES
        method = src.get
        if arg.endswith("[]"): arg = arg[:-2]; method = src.getlist

        if arg in src:
            kwargs[arg] = method(arg)
    try:
        response = service(**kwargs)
    except ServiceException, e:
        response = e.response
        status = e.status
    except Exception, e:
        return HttpResponse("ERROR: %s.%s(%s)" % (e.__class__.__module__, e.__class__.__name__, e), status=getattr(e, "status", 400))
    response = JSONEncoder().encode(response)
    return HttpResponse(response, mimetype="application/json", status=status)





def token(request):
    if not request.user.is_authenticate():
        return HttpResponseRedirect(reverse("xadrpy.core.api.views.authenticate"))

def authorize(request):
    pass

def authenticate(request):
    pass

@api.response(pattern=False, permissions=False)
def get_permissions(request):
    return rights.get_rights_dict()
