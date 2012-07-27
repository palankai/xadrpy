from xadrpy.access import prefs
from xadrpy.contrib.themes.loaders import get_default_theme
from django.contrib.sites.models import Site

class AccessMiddleware(object):
    
    def process_request(self, request):
        request.site = Site.objects.get_current()
