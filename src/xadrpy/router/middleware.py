class RouterMiddleware(object):
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.route = view_kwargs.get("route", None)
        if request.route:
            request.route.permit(request, view_func, view_args, view_kwargs)
            

