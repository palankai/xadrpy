from xadrpy.router.models import Route
import logging
from django.core.urlresolvers import resolve
from django.http import Http404

logger = logging.getLogger("xadrpy.router.middleware")

class RouterMiddleware(object):
    
    def process_request(self, request):
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
        if request.route:
            request.route.permit(request, view_func, view_args, view_kwargs)
            

