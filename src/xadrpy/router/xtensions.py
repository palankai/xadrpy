import base
from django.conf.urls import url, include

class IncludeApplication(base.Application):

    def get_urls(self, kwargs={}):
        return [url(self.route.get_translated_regex(postfix=""), include(self.route.include_name, self.route.namespace, self.route.name), kwargs=kwargs)]
    
class StaticApplication(base.Application):

    def get_urls(self, kwargs={}):
        return [url(self.route.get_translated_regex(), 'xadrpy.routers.views.static', kwargs=kwargs)]

class TemplateApplication(base.Application):

    def get_urls(self, kwargs={}):
        return [url(self.route.get_translated_regex(), 'xadrpy.routers.views.template', kwargs=kwargs)]

class RedirectApplication(base.Application):

    def get_urls(self, kwargs={}):
        return [url(self.route.get_translated_regex(), 'xadrpy.routers.views.redirect', kwargs=kwargs)] 
    
    
    
    