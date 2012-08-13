# -*- coding: utf-8 -*-
"""
Router támoagató könyvtár
"""
from xadrpy.management.libs import SubCommand
from models import Route
import hashlib

__all__ = ["MetaHandler","Application"]


def update_signatures():
    for route in Route.objects.all(): 
        route.signature = hashlib.md5(route.get_signature()).hexdigest()
        route.save()

class MetaHandler(object):
    """
    Kiindulási meta kezelő osztály
    
    Célja, hogy a route (és leszármazottai) objektum képességei dinamikusan bővíthetőek legyenek.
    Segítségével nem kell egy-egy új attributum felvételekor módosítani az osztályt,
    valamint csökkenti a függőségeket, mivel akár a Route ősosztályt is egy alosztály igényei szerint
    később könnyen lehet bővíteni.
    """
    
    def __init__(self, route):
        """
        Osztály konstruktor
        Másolatot készít a route-ból származó meta adatokról, hogy az alapértelmezések beállítása ne okozzon gondot
        
        :param route: az a route, amit éppen kezel 
        """
        self._route = route
        self._master = route.get_master() and route.get_master().get_meta() or None
        self._parent = route.get_parent() and route.get_parent().get_meta() or None
        self.meta = dict(route.meta)
        self.translated = dict(route.translation().meta)
        self.set_defaults()
    
    def get_route(self):
        """
        Visszaadja a route-ot
        """
        return self._route
    
    def get_master(self):
        """
        Visszaadja a master meta kezelőjét
        """
        return self._master
    
    def get_parent(self):
        """
        Visszaadja a szülő meta kezelőjét
        """
        return self._parent
        
    def set_defaults(self):
        """
        Alapértékek beállítása, figyelembe veszi, hogy a fordított adatokat is vissza kellhet adni
        """
        self.meta.setdefault("menu_title", "")
        self.meta.setdefault("overwrite_meta_title", False)
        self.meta.setdefault("meta_title", "")
        self.meta.setdefault("meta_keywords", "")
        self.meta.setdefault("meta_description", "")
        
        self.translated.setdefault("menu_title", self.meta['menu_title'])
        self.translated.setdefault("meta_title", self.meta['meta_title'])
        self.translated.setdefault("meta_keywords", self.meta['meta_keywords'])
        self.translated.setdefault("meta_description", self.meta['meta_description'])
    
    def get_title(self):
        return self.get_route().get_title()
    
    def get_menu_title(self):
        return self.translated['menu_title'] or self.get_title()
    
    def get_meta_title(self):
        if self.meta.get("overwrite_meta_title") and self.meta.get("meta_title"):
            return self.translated.get("meta_title")
        
        self_title = self.translated.get("meta_title") or self.get_title() 
        if self.get_parent() and self.get_parent().get_meta_title():
            self_title = self_title + " | " + self.get_parent().get_meta_title()
        return self_title

    def get_meta_keywords(self):
        if self.meta.get('meta_keywords'):
            return self.meta.get("meta_keywords")
        return self.get_parent() and self.get_parent().get_meta_keywords() or "" 

    def get_meta_description(self):
        if self.meta.get("meta_description"):
            return self.meta.get("meta_description")
        return self.get_parent() and self.get_parent().get_meta_description() or "" 
    
class RouterCommands(SubCommand):

    def register(self):
        _init = self.command.add_subcommand(self.init, "router.init", help="Update signatures")

    def init(self, **kwargs):
        update_signatures()
