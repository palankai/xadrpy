from models import Route
import logging
from django.core.urlresolvers import resolve
from django.http import Http404
from django.core.signals import request_finished
from django.dispatch.dispatcher import receiver
from django.core.handlers.wsgi import WSGIHandler
from xadrpy.utils.reload import reload_wsgi
import conf
from xadrpy.core.router.base import get_local_request

logger = logging.getLogger("xadrpy.core.router.middleware")

class RouterMiddleware(object):
    
    def process_request(self, request):
        setattr(conf._local, "request", request)
        try:
            resolved = resolve(request.path_info)
            view_kwargs = resolved.kwargs
            route_id = view_kwargs.get("route_id", None)
            if route_id:
                request.route = Route.objects.get(pk=route_id).descendant 
            else:
                request.route = None
        except (Http404, Route.DoesNotExist):
            pass
    
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        view_kwargs.pop("route_id",None)
    
    def process_response(self, request, response):
        #logger.debug("Request: %s", type(get_local_request()))
        if hasattr(conf._local, "need_wsgi_reload"):
            delattr(conf._local, "need_wsgi_reload")
            logger.debug("We have catch need_wsgi_reload flags")
            @receiver(request_finished, sender=WSGIHandler, weak=False, dispatch_uid="xadrpy.core.router.middleware.request_finished_handler")
            def request_finished_handler(sender, **kwargs):
                logger.info("WSGI reloading...")
                reload_wsgi(request)
        return response




