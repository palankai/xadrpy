# -*- coding: utf-8 -*-
import conf
from xadrpy import router
import logging
from django.utils import simplejson 
from copy import deepcopy
import defaults
logger = logging.getLogger("xadrpy.contrib.themes.libs")

def get_library_config_over_default(library):
    return defaults.config(defaults.fallback(library, "name"))
 
def get_library_meta_over_default(obj):
    return defaults.library(obj)

def get_theme_config_over_default(theme):
    return defaults.config(defaults.fallback(theme, "name")) 
    
def get_theme_meta_over_default(obj):
    obj = defaults.theme(obj, translated=defaults.translation)

    layouts = []
    skins = []
    templates = {}
    media = {}
    files = defaults.files()

    for item in obj['layouts']:
        layouts.append(defaults.layout(defaults.fallback(item, "name")))
    
    for item in obj['skins']:
        skins.append(_get_theme_skin_over_default(defaults.fallback(item,"name",source=[item])))

    for name, item in obj['templates'].items():
        templates[name] = defaults.template(defaults.fallback(item,"source"))

    for name, item in obj['media'].items():
        media[name] = defaults.media(defaults.fallback(item,"source"))

    obj['files']=defaults.files(obj['files'])
    for file_type,file_list in files.items():
        for file_def in obj['files'][file_type]:
            file_list.append(defaults.file_defaults(file_def, file_type))

    for f in files['html']:
        if f['name'] not in templates:
            templates[f['name']] = defaults.template({'source': f['name']})


    for f in files['media']:
        if f['name'] not in media:
            media[f['name']] = defaults.media({'source': f['name']})

    
    obj['files'] = files
    obj['layouts'] = layouts
    obj['skins'] = skins
    obj['templates'] = templates
    obj['media'] = media
        
    return obj


def _get_theme_skin_over_default(obj):
    obj = defaults.skin(obj) 
    if isinstance(obj['source'],basestring):
        obj['source']=[obj['source']]
    return obj

class ThemeMetaHandler(router.MetaHandler):
        
    def set_defaults(self):
        super(ThemeMetaHandler, self).set_defaults()
        self.meta.setdefault("layout_name", None)
        self.meta.setdefault("skin_name", None)
        
    def setup_theme(self, theme, request, view, args, kwargs):
        pass
    
    def get_layout_name(self):
        """
        Visszaadja a kiválasztott layout nevét - fallback-el a master majd a parent layout nevére
        """
        layout_name = self.meta.get("layout_name")
        if not layout_name and self.get_master():
            layout_name = self.get_master().get_layout_name()
        if not layout_name and self.get_parent():
            layout_name = self.get_parent().get_layout_name()
        self.meta['layout_name']=layout_name
        return layout_name

    def get_skin_name(self):
        """
        Visszaadja a kiválasztott skin nevét - fallback-el a master majd a parent skin nevére
        """
        skin_name = self.meta.get("skin_name")
        if not skin_name and self.get_master():
            skin_name = self.get_master().get_skin_name()
        if not skin_name and self.get_parent():
            skin_name = self.get_parent().get_skin_name()
        self.meta['skin_name']=skin_name
        
        return skin_name
