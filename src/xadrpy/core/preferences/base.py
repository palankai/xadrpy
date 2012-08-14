from xadrpy.utils.jsonlib import JSONEncoder
from xadrpy.utils.key_string import key_string, key_string_set

class Prefs( object ):
    
    def __init__(self, instance, store, **opts):
        self.instance = instance
        self.store = store
        self.opts = opts

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
        
    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return iter(self.store)

    def __contains__(self, key):
        return self.contains(key)

    def __repr__(self):
        return self.store.__repr__()

    def _underscore_key(self, key):
        return key.replace(".","__")
    
    def _dotted_key(self, key):
        return key.replace("__",".")

    def get(self, key, default=None):
        if self.has_getter(key):
            return self.getter(key)
        return self._get(key, default)
    
    def _get(self, key, default=None):
        return key_string(self.store, self._dotted_key(key), default)
    
    def set(self, key, value):
        if self.has_setter(key):
            return self.setter(key, value)
        self._set(key, value)

    def _set(self, key, value):
        key_string_set(self.store, key, value)
    
    def has_getter(self, key, **opts):
        return hasattr(self, "get_"+self._underscore_key(key))
    
    def getter(self, key, **opts):
        return getattr(self, "get_"+self._underscore_key(key))(**opts)

    def has_setter(self, key, **opts):
        return hasattr(self, "set_"+self._underscore_key(key))
    
    def setter(self, key, value, **opts):
        return getattr(self, "set_"+self._underscore_key(key))(value, **opts)

    
    def delete(self, key):
        if self.contains(key):
            del self.store[key]

    def reset(self, key, value):
        if value is not None:
            self.set(key, value)
        else:
            self.delete(key)
    
    def contains(self, key):
        return key in self.store
    
    def store(self, data):
        for key, value in data.items():
            self.reset(key, value)
    
    def keys(self):
        return self.store.keys()

    def to_json(self):
        return JSONEncoder().encode(self.store)

