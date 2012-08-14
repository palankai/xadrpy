from django.db import models
import conf

class PluginStoreManager(models.Manager):
    
    def get_plugin(self, name):
        if name in conf._plugin_cache:
            return conf._plugin_cache[name] 
        store = self.get(models.Q(plugin=name)|models.Q(alias=name))
        conf._plugin_cache[store.plugin] = store
        conf._plugin_cache[store.alias] = store
        return store
