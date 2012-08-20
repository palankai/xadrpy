
class ThemingMiddleware(object):
    
    def process_request(self, request):
        layout = "@base"
        skin = None
        if hasattr(request, "route") and request.route:
            route = request.route
            skin = route.prefs.get("skin_name")
            layout_name = route.prefs.get("layout_name")
            if layout_name:
                layout = "@"+layout_name
        request.theming_layout = layout
        request.theming_skin = skin
