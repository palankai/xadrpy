from base import Theme
import conf

class ThemeStore(object):
    _instance = None
    
    def __init__(self):
        self._themes = {}
        self._first_theme = None
        
    def register(self, name, theme_def):
        theme = Theme.create(name, theme_def)
        if not self._first_theme:
            self._first_theme = theme
        self._themes[name]=theme
    
    def get_current_theme(self):
        if conf.SELECTED_THEME:
            return self._themes[conf.SELECTED_THEME]
        else:
            return self._first_theme
    
    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        cls._instance = cls()
        return cls._instance

def get_theme_store():
    return ThemeStore.get_instance()

def get_current_theme():
    theme_store = ThemeStore.get_instance()
    return theme_store.get_current_theme()