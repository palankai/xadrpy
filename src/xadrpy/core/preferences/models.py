from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from xadrpy.core.models.fields.nullchar_field import NullCharField
from xadrpy.core.models.fields.object_field import ObjectField
from managers import PrefManager
import datetime
from django.utils.translation import get_language
from xadrpy.core.models.fields.dict_field import DictField
from django.utils.translation import ugettext_lazy as _

class Pref(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    timeout = models.PositiveIntegerField(default=0)

    key = models.CharField(max_length=255, verbose_name=_("Key"), editable=False)

    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, editable=False, related_name="+")
    group = models.ForeignKey(Group, verbose_name=_("Group"), blank=True, null=True, editable=False, related_name="+")
    user = models.ForeignKey(User, verbose_name=_("User"), blank=True, null=True, editable=False, related_name="+")
    namespace = NullCharField(max_length=64, verbose_name=_("Namespace"), editable=False)
    language_code = NullCharField(max_length=5, verbose_name=_("Language code"), editable=False)
    
    meta = DictField(_("Meta data"))
    value = ObjectField(_("Value"))
    
    objects = PrefManager()

    class Meta:
        verbose_name = _("Preferences")
        verbose_name_plural = _("Preferences")
        db_table = "xadrpy_preferences_pref"
        unique_together = ("key", "site","group","user", "namespace", "language_code")

    def __unicode__(self):
        return self.title or "%s# %s" % (self.id, self.key)
    
    def is_valid(self):
        if self.timeout == 0: return True
        return datetime.datetime.now() >= self.modified+datetime.timedelta(seconds=self.timeout)

    def set_value(self, value, language_code=None):
        if not language_code:
            self.value = value
            self.save()
        if language_code:
            alternative = self.get_alternative(language_code)
            alternative.value = value
            alternative.save() 
    
    def get_value(self, language_code=None):
        if not language_code:
            return self.value
        if language_code == True:
            language_code = get_language()
        try:
            alternative = self.alternatives.get(language_code=language_code)
            return alternative.value
        except PrefAlternative.DoesNotExist:
            return self.value
        
    def set_initial_value(self, value, meta=None):
        self.value = value
        self.meta = meta
        self.save()
        
    def set_initial_alternative(self, language_code, value, meta=None):
        alternative, created = self.get_or_create_alternative(language_code)
        if created:
            alternative.meta = meta
            alternative.value = value
            alternative.save()

    def get_alternative(self, language_code):
        alternative, unused = self.get_or_create_alternative(language_code)
        return alternative

    def get_or_create_alternative(self, language_code):
        return PrefAlternative.objects.get_or_create(pref=self, language_code=language_code)
    

class PrefAlternative(models.Model):
    pref = models.ForeignKey(Pref, related_name="alternatives")
    language_code = models.CharField(max_length=5, verbose_name=_("Language code"), editable=False)
    meta = DictField(_("Meta data"))
    value = ObjectField(_("Value"))
    
    class Meta:
        verbose_name = _("Preferences alternative")
        verbose_name_plural = _("Preferences alternatives")
        db_table = "xadrpy_preferences_pref_alternative"
        unique_together = ("pref","language_code")

