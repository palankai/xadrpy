from django.db import models
from xadrpy.core.models.fields.nullchar_field import NullCharField
from xadrpy.core.models.fields.stringset_field import StringSetField
from xadrpy.core.preferences.fields import PrefsStoreField
from managers import PluginStoreManager
from xadrpy.utils.imports import get_class
from xadrpy.core.models.inheritable import TreeInheritable
from xadrpy.core.access.models import OwnedModel
from xadrpy.core.models.fields.language_code_field import LanguageCodeField
from django.utils.translation import ugettext_lazy as _
import conf

class PluginStore(models.Model):
    plugin = models.CharField(max_length=255, unique=True)
    alias = NullCharField(max_length=255, db_index=True)
    slots = StringSetField()
    prefs_store = PrefsStoreField("prefs")
    enabled = models.BooleanField(default=True)
    
    objects = PluginStoreManager()

    class Meta:
        verbose_name = _("Plugin store")
        verbose_name_plural = _("Plugin store")
        db_table = "xadrpy_plugins_store"
    
    def get_plugin_cls(self):
        return get_class(self.plugin)
    
    def get_instance(self, *args, **kwargs):
        cls = self.get_plugin_cls()
        instance = cls(*args, **kwargs)
        instance.set_store(self) 
        return instance
    
    def save(self, force_insert=False, force_update=False, using=None):
        models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using)
        conf._plugin_cache.pop((self.plugin,), None)
        conf._plugin_cache.pop((self.alias,), None)

class PluginPlace(TreeInheritable, OwnedModel):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    store = models.ForeignKey(PluginStore)
    placeholder = NullCharField(max_length=255, unique=True) 
    prefs_store = PrefsStoreField("prefs")
    language_code = LanguageCodeField(default=None, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Plugin place")
        verbose_name_plural = _("Plugin places")
        db_table = "xadrpy_plugins_place"
    
    def __unicode__(self):
        return self.key
    
    def get_instance(self, *args, **kwargs):
        instance = self.store.get_instance(*args, **kwargs)
        instance.set_instance(self.descendant)
