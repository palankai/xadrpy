import types

class Annotable(object):
    def __new__(cls, *args, **kwargs):
        instance = super(Annotable, cls).__new__(cls, *args, **kwargs)
        instance._annoted = []
        for name in dir(instance): 
            if isinstance(getattr(instance,name), types.MethodType) and hasattr(getattr(instance, name), "_annotations"):
                instance._annoted.append(getattr(instance,name))
        return instance
    
    def get_annoted_methods(self, annotation_cls=None):
        if not annotation_cls:
            return [(method, method._annotations) for method in self._annoted]

        result = []
        for method in self._annoted:
            entry = (method, [])        
            for annotation in method._annotations:
                if isinstance(annotation, annotation_cls):
                    entry[1].append(annotation)
            if len(entry[1]):
                result.append(entry)
        return result

class Annotation(object):

    def __new__(cls, func=None, **kwargs):
        instance = super(Annotation, cls).__new__(cls, func, **kwargs)
        instance.__init__(**kwargs)
        def inner(func):
            if hasattr(func, "_annotations"):
                func._annotations.append( instance )
            else:
                func._annotations = [ instance ]
            return func

        if func:
            return inner(func)
        else:
            return inner
        
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
