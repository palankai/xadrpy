from django.db import models
from xadrpy.models.inheritable import Inheritable
from xadrpy.models.fields.json_field import JSONField
from django.utils.translation import ugettext_lazy as _
from xadrpy.utils.signals import autodiscover_signal
from django.dispatch.dispatcher import receiver
import conf
from xadrpy.utils.imports import get_class
from django.db.models import Q

class Theme(Inheritable):
    name = models.CharField(max_length=255, unique=True)
    meta = JSONField()
    utime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name=_("Theme")
        verbose_name_plural=_("Themes")
        db_table = "xadrpy_themes_theme"

    def get_base_path(self):
        if hasattr(self, "_base_path"):
            return self._base_path
        self._base_path = "themes/%s/" % (self.meta['name'])
        if self.meta['type']:
            self._base_path = "%s/%s" % (self.meta['type'], self._base_path)
        return self._base_path

    def get_base_html(self):
        return self.get_base_path() + self.meta['layouts'][0]['name']
    
    def get_styles(self):
        for style in self.meta['styles']:
            yield self.get_base_path() + style
    
    def get_scripts(self):
        for script in self.meta['scripts']:
            yield self.get_base_path() + script
        
    def get_libraries(self):
        libs = self.meta['libs']+conf.DEFAULT_LIBRARIES
        return Library.objects.filter(Q(autoload=True)|Q(name__in=libs))

    def templates(self):
        print self.meta['templates']
        return dict([(template['name'], self.get_base_path()+template['source']) for template in self.meta['templates']])

class Library(Inheritable):
    name = models.CharField(max_length=255, unique=True)
    autoload = models.BooleanField(default=False, db_index=True)
    meta = JSONField()
    utime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name=_("Library")
        verbose_name_plural=_("Libraries")
        db_table = "xadrpy_themes_library"

    def get_styles(self):
        for style in self.meta['styles']:
            yield self.get_base_path() + style

    def get_scripts(self):
        for script in self.meta['scripts']:
            yield self.get_base_path() + script


    def get_base_path(self):
        if hasattr(self, "_base_path"):
            return self._base_path
        self._base_path = "libs/"
        if self.meta['type']:
            self._base_path = "%s/%s" % (self.meta['type'], self._base_path)
        return self._base_path


@receiver(autodiscover_signal)
def init_theme_loaders(**kwargs):
    import loaders
    
    for loader_name in conf.THEME_LOADERS:
        loader_cls = get_class(loader_name, loaders.ThemeLoader)
        loader = loader_cls()
        loader.load()
