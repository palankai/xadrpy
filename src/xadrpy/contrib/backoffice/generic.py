from django.template.loader import render_to_string
from django.template.context import RequestContext
import logging
logger = logging.getLogger("BackOffice.generic")

class Manager(object):
    def __init__(self):
        self._items = []
    
    def register(self, item):
        self._items.append(item)
        logger.info("Register: %s", item.__class__.__name__)
        
    def get_items(self):
        return self._items
    
store_manager = Manager()

class Store(object):
    template = "xadrpy/backoffice/generic/store.js"
    name = None
    autoload = False
    url = ""
    fields = []
    
    def render(self, request):
        ctx = {
            'name': self.name,
            'autoload': self.autoload,
            'url': self.url,
            'fields': self.fields, 
        }
        return render_to_string(self.template, ctx, RequestContext(request))
