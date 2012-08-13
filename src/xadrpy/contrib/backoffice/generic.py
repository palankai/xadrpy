import logging
logger = logging.getLogger("xadrpy.contrib.backoffice.generic")

class Manager(object):
    def __init__(self):
        self._items = []
    
    def register(self, item):
        self._items.append(item)
        
    def get_items(self):
        return self._items
    
model_manager = Manager()
store_manager = Manager()
