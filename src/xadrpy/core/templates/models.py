#from django.db import models
#from django.utils.translation import ugettext_lazy as _
#from xadrpy.core.i18n.models import Translation
#from xadrpy.core.i18n.fields import TranslationForeignKey
#import logging
#
#logger = logging.getLogger("xadrpy.templates.models")

        

        
        
#class SnippetInstance(PluginInstance):
#    body = models.TextField(blank=True, null=True)
#    
#    class Meta:
#        verbose_name = _("Snippet Plugin")
#        verbose_name_plural = _("Snippet Plugins")
#        db_table = "xadrpy_templates_snippet_instance"
#
#class SnippetTranslation(Translation):
#    origin = TranslationForeignKey(SnippetInstance, related_name="+")
#    language_code = models.CharField(max_length=5)
#
#    body = models.TextField(blank=True, null=True)
#
#    class Meta:
#        db_table = "xadrpy_pages_snippet_instance_translation"
#
#SnippetTranslation.register(SnippetInstance)
