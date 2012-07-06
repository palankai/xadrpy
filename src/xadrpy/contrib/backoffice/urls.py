from django.conf.urls.defaults import patterns, url, include
import logging
import conf
logger = logging.getLogger("BackOffice")

urlpatterns = patterns('xadrpy.contrib.backoffice.views',
    url(r'^$', 'backoffice'),
    url(r'^login/$', 'extlogin'),
    url(r'^logout/$', 'logout'),
    url(r'^generic/$', 'generic'),
)

def backoffice_autodiscover():
    import imp
    from django.conf import settings

    from django.utils import importlib

    for app in settings.INSTALLED_APPS:
        
        try:                                                                                                                          
            app_path = importlib.import_module(app).__path__                                                                          
        except AttributeError:                                                                                                        
            continue 
        
        try:                                                                                                                          
            imp.find_module('backoffice', app_path)                                                                               
        except ImportError:                                                                                                           
            continue                                                                                                               
        module = importlib.import_module("%s.backoffice" % app)

        if hasattr(module, "NAMESPACES"):
            conf.NAMESPACES.update(module.NAMESPACES)
        
        if hasattr(module, "CONTROLLERS"):
            conf.CONTROLLERS.extend(module.CONTROLLERS)
            
backoffice_autodiscover()        
        
