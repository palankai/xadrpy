from xadrpy.contrib.themes.loaders import get_default_theme
from xadrpy.contrib.themes.models import ThemeAdjuster
from xadrpy.contrib.themes.libs import ThemeMetaHandler

class ThemeMiddleware(object):
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.theme = get_default_theme(request.user.is_authenticated() and request.user or None)
        if request.route and isinstance(request.route, ThemeAdjuster) or hasattr(request.route, "setup_theme"):
            request.route.setup_theme(request.theme, request, view_func, view_args, view_kwargs)
        elif request.route:
            meta_handler = request.route.get_meta()
            assert isinstance(meta_handler, ThemeMetaHandler)
            meta_handler.setup_theme(request.theme, request, view_func, view_args, view_kwargs)

