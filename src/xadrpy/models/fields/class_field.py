import logging
from xadrpy.utils.imports import get_class
logger = logging.getLogger("xadrpy.contrib.models.fields.class_field")

class ClassField(object):

    def __init__(self, field=None, default=None, args=[], kwargs={}):
        self.field = field
        self.default = default
        self.args = args
        self.kwargs = kwargs
        
    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name
        cls._meta.add_virtual_field(self)
        setattr(cls, name, self)

    def get_default(self, obj):
        if self.default and callable(self.default):
            return self.default(obj)
        return self.default

    def get_class(self, obj):
        if not self.field:                     return self.get_default(obj)
        if callable(self.field):               return self.field(obj) or self.get_default(obj)
        if not getattr(obj, self.field):       return self.get_default(obj)
        if callable(getattr(obj, self.field)): return getattr(obj, self.field)() or self.get_default(obj)
        return getattr(obj, self.field) or self.get_default(obj)
    
    def get_instance(self, obj):
        cls = self.get_class(obj)
        if not cls: return None
        if isinstance(cls, basestring):
            cls = get_class(cls)
        return cls(obj, *self.args, **self.kwargs)

    def __get__(self, obj, obj_type=None):
        if obj is None: return self
        try:
            return getattr(obj, self.cache_attr)
        except AttributeError:
            try:
                instance = self.get_instance(obj)
            except Exception, e:
                logger.exception("Can't create instance for '%s' - %s", self.name, e)
                instance = None
            setattr(obj, self.cache_attr, instance)
            return instance

    def __set__(self, instance, value):
        raise AttributeError(u"Can't set %s field" % self.name)
