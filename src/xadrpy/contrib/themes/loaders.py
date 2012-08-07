'''
Created on 2012.07.26.

@author: pcsaba
'''
from xadrpy.utils.imports import get_installed_apps_module
from django.conf import settings
import base
import conf 
import models
from django.template.loader import render_to_string
from django.utils import simplejson
import logging
from xadrpy.core.preferences.libs import prefs
logger = logging.getLogger("xadrpy.contrib.themes.loaders")

def get_default_theme(user=None):
    theme_name = prefs(key="default_theme", 
                       namespace="x-themes", 
                       site=0, 
                       user=user,
                       order=['user','site'],
                       default=conf.DEFAULT_THEME)
    return models.Theme.objects.get(name=theme_name)

class ThemeLoader(object):
    
    def load(self):
        pass

    def init_theme_meta(self, meta):
        return base.get_theme_meta_over_default(meta)

    def init_library_meta(self, meta):
        meta = base.get_library_meta_over_default(meta)
        return meta

class StaticThemeLoader(ThemeLoader):
    
    def load(self):
        for theme in getattr(settings, "THEMES", ()):
            self.load_theme(base.get_theme_config_over_default(theme))

        for library in getattr(settings, "LIBRARIES", ()):
            self.load_library(base.get_library_config_over_default(library))

        for conf_module in get_installed_apps_module("conf"):

            for theme in getattr(conf_module, "THEMES", ()):
                self.load_theme(base.get_theme_config_over_default(theme))

            for library in getattr(conf_module, "LIBRARIES", ()):
                self.load_library(base.get_library_config_over_default(library))

    
    def load_theme(self, theme):
        
        if 'layouts' in theme:
            meta = self.init_theme_meta(theme)
        else:
            path = "themes/%s/metadata.json" % theme['name']
            if theme['type']:
                path = theme['type']+"/"+path 
            meta_str = render_to_string(path)
            meta_obj = simplejson.loads(meta_str)
            meta = self.init_theme_meta(meta_obj)
        theme_obj, created = models.Theme.objects.get_or_create(name=theme['name'])
        
        if created or settings.DEBUG:
            theme_obj.meta = meta
            theme_obj.save()
        self.collect_files(theme_obj)

    def load_library(self, library):
        if 'scripts' in library or 'styles' in library:
            meta = self.init_library_meta(library)
        else:
            path = "libs/%s/metadata.json" % library['name']
            if library['type']:
                path = library['type']+"/"+path 

            meta_str = render_to_string(path)
            meta_obj = simplejson.loads(meta_str)
            meta = self.init_library_meta(meta_obj)
        library_obj, created = models.Library.objects.get_or_create(name=library['name'])
        if created or settings.DEBUG:
            library_obj.meta = meta
            library_obj.autoload = meta['autoload']
            library_obj.save()
    
    def collect_files(self, theme):
        theme.collect_files()
        pass
