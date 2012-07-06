from django.conf.urls.defaults import patterns, url, include
import logging
import conf

logger = logging.getLogger("API")


urlpatterns = patterns('',
    url(r'^$', 'xadrpy.api.views.home', name="APIBASE"),
    url(r'^auth/get_permissions/$', 'xadrpy.api.views.get_permissions')
)


def api_autodiscover():
    import imp
    from django.conf import settings

    from django.utils import importlib


    for app in settings.INSTALLED_APPS:
        
        try:                                                                                                                          
            app_path = importlib.import_module(app).__path__                                                                          
        except AttributeError:                                                                                                        
            continue 
        
        try:                                                                                                                          
            imp.find_module('api', app_path)                                                                               
        except ImportError:                                                                                                           
            continue                                                                                                                  
        module = importlib.import_module("%s.api" % app)
        module_name = getattr(module, "API_MODULE_NAME", app)

    for pattern, method, kwargs in conf.urls:
        urlpatterns.append(url(pattern, method, kwargs=kwargs))
        
