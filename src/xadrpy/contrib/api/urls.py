from django.conf.urls.defaults import patterns, url, include
import logging
logger = logging.getLogger("API")

api_urlpatterns = patterns('',
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

        for name in dir(module):
            method = getattr(module, name)
            if hasattr(method, "_api_params"):
                pattern = r"%s/%s" % (module_name, method._api_params['pattern'])
                api_urlpatterns.append(url(pattern, method, kwargs=method._api_params['kwargs']))
                #print pattern
            
        
        
