from xadrpy.router.base import Application

class BlogApplication(Application):

    def get_urls(self, kwargs={}):
        resolver = self.route.get_resolver()
        return resolver.get_urls(kwargs)
