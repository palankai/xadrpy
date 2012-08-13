import logging
from xadrpy.core.models.fields.class_field import ClassField
from xadrpy.core.preferences.base import Prefs
from xadrpy.core.models.fields.dict_field import DictField
logger = logging.getLogger("xadrpy.core.preferences.fields")

class PrefsField(ClassField):
    
    def __init__(self, store, field=None, ifnull=None, fallback=None, opts={}):
        self.store = store
        if not fallback and not ifnull:
            ifnull=Prefs
        ClassField.__init__(self, field, ifnull, fallback, opts)

    def create_instance(self, obj, cls, opts):
        store = getattr(obj, self.store)
        return cls(obj, store, **opts)

        

class PrefsStoreField(DictField):
    
    def __init__(self, attrib_name=None, field=None, ifnull=None, fallback=None, opts={}, **kwargs):
        self.attrib_name = attrib_name
        self.field = field
        self.ifnull = ifnull
        self.fallback = fallback
        self.opts = opts
        super(PrefsStoreField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        DictField.contribute_to_class(self, cls, name)
        
        if not self.attrib_name:
            tmp_name = ("%s_%s" % (cls.__name__,name)).lower()
            if not hasattr(cls, tmp_name):
                self.attrib_name = tmp_name
        if self.attrib_name:
            class_field = PrefsField(store=name, field=self.field, ifnull=self.ifnull, fallback=self.fallback, opts=self.opts)
            class_field.contribute_to_class(cls, self.attrib_name)
            

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core.\preferences\.fields\.PrefsStoreField"])
