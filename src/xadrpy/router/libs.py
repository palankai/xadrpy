# -*- coding: utf-8 -*-
__all__ = ["MetaHandler","Application"]
"""
Router támoagató könyvtár
"""

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
        
        self.translated.setdefault("menu_title", self.meta['menu_title'])
    
    def get_menu_title(self):
        return self.translated['menu_title'] or self.get_route().title

class Application(object):
    def __init__(self, route):
        self._route = route
    
    def get_route(self):
        return self._route
    
    def get_urls(self, kwargs):
        return []
    
    route = property(get_route)
