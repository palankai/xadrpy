from django.db import models
from xadrpy.models.fields.nullchar_field import NullCharField
from xadrpy.models.fields.stringset_field import StringSetField
from django.utils.translation import ugettext_lazy as _
from xadrpy.access.models import OwnedModel
from xadrpy.i18n.models import Translation
from xadrpy.i18n.fields import TranslationForeignKey
from xadrpy.models.inheritable import TreeInheritable
import logging
logger = logging.getLogger("xadrpy.templates.models")

class PluginStore(models.Model):
    plugin = models.CharField(max_length=255, unique=True)
    template = NullCharField(max_length=255)
    slots = StringSetField()

    class Meta:
        verbose_name = _("Plugin store")
        verbose_name_plural = _("Plugin store")
        db_table = "xadrpy_templates_plugin_store"

class PluginInstance(TreeInheritable, OwnedModel):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))

    plugin = models.CharField(max_length=255)
    placeholder = NullCharField(max_length=255)

    slot = NullCharField(max_length=255)
    position = models.IntegerField(default=1)

    language_code = NullCharField(max_length=5)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Plugin")
        verbose_name_plural = _("Plugins")
        db_table = "xadrpy_templates_plugin_instance"
    
    def __unicode__(self):
        return self.key
        
class SnippetInstance(PluginInstance):
    body = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Snippet Plugin")
        verbose_name_plural = _("Snippet Plugins")
        db_table = "xadrpy_templates_snippet_instance"

class SnippetTranslation(Translation):
    origin = TranslationForeignKey(SnippetInstance, related_name="+")
    language_code = models.CharField(max_length=5)

    body = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "xadrpy_pages_snippet_instance_translation"

SnippetTranslation.register(SnippetInstance)
