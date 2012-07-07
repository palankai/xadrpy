from django.template.loader import render_to_string
from django.template.context import RequestContext
import logging
from xadrpy.api.decorators import APIObject
from django.core.urlresolvers import reverse
logger = logging.getLogger("BackOffice.generic")

class Manager(object):
    def __init__(self):
        self._items = []
    
    def register(self, item):
        self._items.append(item)
        
    def get_items(self):
        return self._items
    
model_manager = Manager()
store_manager = Manager()
