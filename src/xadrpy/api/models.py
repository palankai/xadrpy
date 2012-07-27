from xadrpy.utils.signals import autodiscover_signal
from django.dispatch.dispatcher import receiver
import conf
from urls import urlpatterns
from django.conf.urls.defaults import url

@receiver(autodiscover_signal)
def api_autodiscover(**kwargs):
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
