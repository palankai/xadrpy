from xadrpy.management.libs import SubCommand
from models import PluginStore
import base

class PluginsCommands(SubCommand):

    def register(self):
        _init = self.command.add_subcommand(self.init, "plugins.init", help="Init plugins, ...")
        _reset = self.command.add_subcommand(self.reset, "plugins.reset", help="Reset plugins, ...")

    def reset(self, **kwargs):
        PluginStore.objects.all().delete()
        self.init(**kwargs)

    def init(self, **kwargs):
        import imp
        from django.utils import importlib
        from django.conf import settings
        from inspect import isclass
        
        for app in settings.INSTALLED_APPS:
            
            try:                                                                                                                          
                app_path = importlib.import_module(app).__path__                                                                          
            except AttributeError:                                                                                                        
                continue 
            
            try:                                                                                                                          
                imp.find_module('xtensions', app_path)                                                                               
            except ImportError:                                                                                                           
                continue                                                                                                                  
            module = importlib.import_module("%s.xtensions" % app)
            for name in dir(module):
                cls = getattr(module,name)
                if isclass(cls) and issubclass(cls, base.Plugin) and cls!=base.Plugin:
                    store, unused = PluginStore.objects.get_or_create(plugin=cls.get_name())
                    store.alias = cls.alias
                    store.save()
