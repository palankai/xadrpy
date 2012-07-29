from xadrpy.router.models import Route
class RouterMiddleware(object):
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.route = view_kwargs.get("route", None)
        if request.route:
            if isinstance(request.route, (int, long)):
                request.route = Route.objects.get(pk=request.route).descendant
                view_kwargs['route'] = request.route
            request.route.permit(request, view_func, view_args, view_kwargs)
            

