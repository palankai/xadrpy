import os
from django.utils.datastructures import SortedDict
from copy import copy

class Theme(object):
    static_path = None
    template_path = None
    
    def __init__(self, name, config):
        self.name = name
        self.__dict__.update(config)
        self.layouts = SortedDict(getattr(self, "layouts", {}))
        self.skins = SortedDict(getattr(self, "skins", {}))
         
    
    def get_layout_template(self, name):
        if name=="base":
            return os.path.join(self.template_path, self.base)
        if not name in self.layouts:
            return os.path.join(self.template_path, name+".html")
        return os.path.join(self.template_path, self.layouts[name]['file'])
    
    def get_skin_styles(self, name):
        if not name: return []
        if name not in self.skins:
            return [{"file": self.static_path+"/"+name+".css"}]
        return self.skins[name]['styles']

    def get_skin_scripts(self, name):
        if not name or \
           not name in self.skins or \
           not 'scripts' in self.skins: return []
        return self.skins[name]['scripts']
    
    def get_rewrite(self, layout_name, skin_name):
        rewrite = copy(getattr(self, "rewrite", {}))
        if layout_name and layout_name in self.layouts:
            rewrite.update(self.layouts[layout_name].get("rewrite", {}))
        if skin_name and skin_name in self.skins:
            rewrite.update(self.skins[skin_name].get("rewrite", {}))
        return rewrite
    
    @classmethod
    def create(cls, name, config):
        theme = cls(name, config)
        return theme

