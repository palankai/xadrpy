from xadrpy.access import prefs
from xadrpy.contrib.themes.loaders import get_default_theme

class ThemeMiddleware(object):
    
    def process_request(self, request):
        request.theme = get_default_theme(request.user.is_authenticated() and request.user or None)
