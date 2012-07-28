# -*- coding: utf-8 -*-
import conf
from xadrpy import router
import logging
logger = logging.getLogger("themes")

def get_theme_config_over_default(theme):
    return dict(conf.BASE_CONFIG, **_fallback(theme))

def get_library_config_over_default(library):
    return dict(conf.BASE_CONFIG, **_fallback(library))
    
def get_theme_meta_over_default(obj):
    obj = dict(conf.BASE_THEME, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    layouts = []
    skins = []
    templates = {}
    media = {}
    
    for item in obj['layouts']:
        layouts.append(_get_theme_layout_over_default(_fallback(item)))
    
    for item in obj['skins']:
        skins.append(_get_theme_skin_over_default(_fallback(item)))

    obj['files']=dict(conf.BASE_FILES, **obj['files'])
    files = dict(conf.BASE_FILES)
    for k,v in files.items():
        for f in obj['files'][k]:
            v.append(dict(conf.BASE_FILE_DEFAULTS[k], **f))
    logger.debug(files)
    
    for name, item in obj['templates'].items():
        templates[name] = _get_theme_template_over_default(_fallback(item,"source"))

    for f in files['html']:
        if f['name'] not in templates:
            templates[f['name']] = _get_theme_template_over_default({'source': f['name']})

    for name, item in obj['media'].items():
        media[name] = _get_theme_media_over_default(_fallback(item,"source"))

    for f in files['media']:
        if f['name'] not in media:
            media[f['name']] = _get_theme_media_over_default({'source': f['name']})

    
    obj['files'] = files
    obj['layouts'] = layouts
    obj['skins'] = skins
    obj['templates'] = templates
    obj['media'] = media
        
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

def _get_theme_media_over_default(obj):
    obj = dict(conf.BASE_MEDIA, **obj)
    obj['translated'] = _get_translation_over_default(obj['translated'])
    return obj


def _get_translation_over_default(obj):
    return dict(conf.BASE_THEME_TRANSLATION, **obj)

def _fallback(obj, name="name"):
    return isinstance(obj, basestring) and {name: obj} or obj

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
