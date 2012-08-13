from nullchar_field import NullCharField
from xadrpy.utils.imports import get_class
from django.db import models
import logging
from inspect import isclass

logger = logging.getLogger("xadrpy.core.models.fields.class_field")

class BaseClass(object):
    def __init__(self, instance, **opts):
        self.instance = instance

class ClassField(object):

    def __init__(self, field=None,  ifnull=None, fallback=None, opts={}):
        self.field = field
        self.ifnull = ifnull
        self.fallback = fallback
        self.opts = opts
        
    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name
        cls._meta.add_virtual_field(self)
        setattr(cls, name, self)

    def get_class(self, obj):
        #return a class name what is stored in the field
        if self.field and getattr(obj, self.field):
            return getattr(obj, self.field)
        #return alternative of default
        if self.ifnull:
            return self.ifnull
        #return none of not given self.fallback
        if not self.fallback:
            return None
        #return obj.fallback or obj.fallback()
        if isinstance(self.fallback, basestring):
            fallback_member = getattr(obj, self.fallback)
            if callable(fallback_member):
                return fallback_member()
            return fallback_member
        #return self.fallback given a class 
        if isclass(self.fallback):
            return self.fallback
        if callable(self.fallback):
            return self.fallback(obj)
        return None
    
    def get_opts(self, obj):
        if isinstance(self.opts, dict):
            return self.opts
        if isinstance(self.opts, basestring):
            opts_member = getattr(obj, self.opts)
            if callable(opts_member):
                return opts_member()
            return opts_member
        if callable(self.opts):
            return self.opts(obj)
    
    def get_instance(self, obj):
        cls = self.get_class(obj)
        if not cls: return None
        if isinstance(cls, basestring):
            cls = get_class(cls)
        opts = self.get_opts(obj) or {}
        return self.create_instance(obj, cls, opts)
    
    def create_instance(self, obj, cls, opts):
        return cls(obj, **opts)

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


class ClassNameField(NullCharField):
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, attrib_name, ifnull=None, fallback=None, opts={}, **kwargs):
        self.attrib_name = attrib_name
        self.ifnull = ifnull
        self.fallback = fallback
        self.opts = opts
        kwargs.setdefault("max_length", 255)
        kwargs.setdefault("default", None)
        super(ClassNameField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        NullCharField.contribute_to_class(self, cls, name)
        class_field = ClassField(field=name, ifnull=self.ifnull, fallback=self.fallback, opts=self.opts)
        class_field.contribute_to_class(cls, self.attrib_name)
        

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.class_name_field\.ClassNameField"])
