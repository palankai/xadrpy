from functools import wraps

def _dict_update_wrapper(_F=None, **kwargs):
    def inner(func):
        @wraps(func)
        def wrapper(_O={},*args, **fkwargs):
            result = dict(func(*args), **_O)
            for k,v in kwargs.items():
                result[k]=v(result[k])  
            for k,v in fkwargs.items():
                result[k]=v(result[k])  
            return result
        return wrapper
    if _F:
        return inner(_F)
    return inner

def fallback(obj, *args, **kwargs):
    if isinstance(obj, dict): return obj
    return dict([(k, obj) for k in args]+[(k,v) for k,v in kwargs.items()])

@_dict_update_wrapper
def translation(): return { 
        "title": None, 
        "description": None, 
        "thumbnail": None
    }


@_dict_update_wrapper
def config(): return {
        "name": None,
        "type": None,
    }
    
@_dict_update_wrapper
def theme(): return {
        "name": None,
        "type": None,
        "doctype": ["HTML5"],
        "thumbnail": None,
        "title": None,
        "description": None,
        "translated": {},
        "features": [],
        "layouts": [],
        "skins": [],
        "default_skin": None,
        "templates": {},
        "media": {},
        "styles": [],
        "scripts": [],
        "libs": [],
        "supported": [],
    }
    
@_dict_update_wrapper
def layout(): return {
        "name": None,
        "source": None,
        "title": None,
        "description": None,
        "thumbnail": None,
        "styles": [],
        "scripts": [],
        "libs": [],
        "translated": {}
    }

@_dict_update_wrapper
def library(): return {
        "name": None,
        "type": None,
        "title": None,
        "description": None,
        "version": None,
        "thumbnail": None,
        "scripts": [],
        "styles": [],
        "translated": {},
        "autoload": False,
    }

@_dict_update_wrapper
def skin(): return {
        "name": None,
        "source": [],
        "title": None,
        "description": None,
        "thumbnail": None,
        "translated": {}
    }

@_dict_update_wrapper
def template(): return {
        "source": None,
        "title": None,
        "description": None,
        "thumbnail": None,
        "translated": {}
    }

@_dict_update_wrapper
def media(): return {
        "source": None,
        "title": None,
        "description": None,
        "thumbnail": None,
        "translated": {}
    }

@_dict_update_wrapper
def files(): return { 
        'html': [], 
        'style': [], 
        'script': [], 
        'media': [] 
    }

@_dict_update_wrapper
def fileinfo():return {
    "name": None,
    "file_name": None,
    "file": None,
    "files": [],
    "files_tripple": [None,None,None],
    "base_file": None,
    "middle_file": None,
    "top_file": None,
    "required": True,
}

@_dict_update_wrapper
def file_defaults(what):
    if what == "style": return fileinfo({"media":None})
    return fileinfo()  
