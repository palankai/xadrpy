# -*- coding: utf-8 -*-
import conf
from xadrpy import router

def get_theme_config_over_default(theme):
    return dict(conf.BASE_CONFIG, **_name_fallback(theme))

def get_library_config_over_default(library):
    return dict(conf.BASE_CONFIG, **_name_fallback(library))
    
def get_theme_meta_over_default(obj):
    obj = dict(conf.BASE_THEME, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    layouts = []
    skins = []
    templates = []
    
    for item in obj['layouts']:
        layouts.append(_get_theme_layout_over_default(_name_fallback(item)))
    
    for item in obj['skins']:
        skins.append(_get_theme_skin_over_default(_name_fallback(item)))

    for item in obj['templates']:
        templates.append(_get_theme_template_over_default(_name_fallback(item)))
    
    obj['layouts'] = layouts
    obj['skins'] = skins
    obj['templates'] = templates
        
    return obj

def get_library_meta_over_default(obj):
    obj = dict(conf.BASE_LIBRARY, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    return obj

def _get_theme_layout_over_default(obj):
    obj = dict(conf.BASE_LAYOUT, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    return obj


def _get_theme_skin_over_default(obj):
    obj = dict(conf.BASE_SKIN, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    return obj

def _get_theme_template_over_default(obj):
    obj = dict(conf.BASE_TEMPLATE, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    return obj

def _get_translation_over_default(obj):
    return dict(conf.BASE_THEME_TRANSLATION, **obj)

def _name_fallback(obj):
    return isinstance(obj, basestring) and {'name': obj} or obj

class ThemeMetaHandler(router.MetaHandler):
        
    def set_defaults(self):
        super(ThemeMetaHandler, self).set_defaults()
        self.meta.setdefault("layout_name", None)
        self.meta.setdefault("skin_name", None)
    
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
