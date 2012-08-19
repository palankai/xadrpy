import conf

class Theme(object):
    static_path = None
    template_path = None
    
    @classmethod
    def get_instance(cls, config):
        theme = cls()
        theme.__dict__.update(config)
        return theme
        
    
class ThemeStore(object):
        
    def register(self, name, theme_def):
        if isinstance(theme_def, dict):
            theme_def = Theme.get_instance(theme_def)
        conf.themes[name]=theme_def

theme_store = ThemeStore() 
