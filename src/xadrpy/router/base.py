
class Application(object):
    
    def __init__(self, route):
        self._route = route
    
    def get_route(self):
        return self._route
    
    def get_urls(self, kwargs):
        return []
    
    route = property(get_route)

