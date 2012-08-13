import logging
from django.dispatch.dispatcher import receiver
from xadrpy.utils.signals import autodiscover_signal

@receiver(autodiscover_signal, dispatch_uid="register_in_store")
def register_in_store(**kwargs):
    import imp
    from django.utils import importlib
    from django.conf import settings
    from inspect import isclass
    import libs
    from models import PluginStore
    
    for app in settings.INSTALLED_APPS:
        
        try:                                                                                                                          
            app_path = importlib.import_module(app).__path__                                                                          
        except AttributeError:                                                                                                        
            continue 
        
        try:                                                                                                                          
            imp.find_module('plugins', app_path)                                                                               
        except ImportError:                                                                                                           
            continue                                                                                                                  
        module = importlib.import_module("%s.plugins" % app)
        for name in dir(module):
            cls = getattr(module,name)
            if isclass(cls) and issubclass(cls, libs.Plugin) and cls!=libs.Plugin:
                store = PluginStore.objects.get(plugin=cls.get_name())
                if store.template:
                    cls.template = store.template
                libs.PLUGIN_CACHE[cls.get_name()]=cls
                if cls.alias:
                    libs.PLUGIN_CACHE[cls.alias]=cls
