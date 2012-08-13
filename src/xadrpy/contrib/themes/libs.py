# -*- coding: utf-8 -*-
import conf
import logging
from xadrpy.management.libs import SubCommand
from django.template.loader import find_template
from xadrpy.core import router
from xadrpy.utils.imports import get_class
from xadrpy.contrib.themes.models import Theme, Library
logger = logging.getLogger("xadrpy.contrib.themes.libs")

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
        layout_name = self.meta.get("layout_name", None)
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

class ThemesCommands(SubCommand):
    
    def register(self):
        _collect = self.command.add_subcommand(self.init, "themes.init", help="Collects themes")
    
    def reset(self, **kwargs):
        Theme.objects.all().delete()
        Library.objects.all().delete()
        self.init(**kwargs)
    
    def init(self, **kwargs):
        self.stdout.write("Collecting themes...\n")
        import loaders, time
        try:
            find_template("xadrpy/themes/base.html") #Hack: init template loaders
            for loader_name in conf.THEME_LOADERS:
                theme_loader_cls = get_class(loader_name, loaders.ThemeLoader)
                theme_loader = theme_loader_cls()
                theme_loader.load()
        except Exception, e:
            logger.exception("Theme loading failed: %s", e)
            return
        
