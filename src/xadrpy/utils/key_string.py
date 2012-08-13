"""
These functions allows set and get value of a dict with a "dot noted" key.
The `key_string_set` functions allow `int` type as key part.
The key part converted to int if can. Empty key part converted to next int key.
When in the current level no keys - next key is '0'
When in the current level no int keys (may just 'a', 'b') - next key is '0'


>>> d={'a':{'b':{'c': 1 }}}
>>> key_string(d, "a.b.c")
1
>>> key_string(d, "a.b")
{'c': 1}
>>> key_string(d, "a.b.d")
None

>>> key_string(d, "a.b.d", "default")
"default"

Set values:
>>> key_string_set(d, "a.b.c", 2)
>>> key_string(d, "a.b.c")
2
>>> key_string_set(d, "a.b.d", 3)
>>> key_string(d, "a.b.d")
3
>>> key_string_set(d, "e.f", 3)
>>> key_string(d, "e")
{"e": 3}

>>> key_string_set(d, "nums.", 1)
>>> key_string_set(d, "nums.", 2)
>>> key_string(d, "nums")
{0: 1}
>>> key_string(d, "nums.0")
{0: 1}
>>> key_string(d, "nums.1")
{0: 2}

"""
STRICT=1

def key_string(source, key, default=None):
    if not key: return source
    keys = key.split( "." )
    keys.reverse()
    if isinstance(source, dict):
        return _key_string(source, keys, default)
    return default

def _key_string(source, keys, default):
    key = keys.pop()
    try: key = int(key) 
    except: pass
    if len( keys ):
        if isinstance( source.get(key), dict ):
            return _key_string(source[key], keys, default)
        else: return default
    return source.get(key, default)


def key_string_set(source, key, value, mode=0):
    if not key or not isinstance(source, dict): raise KeyError("Doesn't specificed key") 
    keys = key.split( "." )
    keys.reverse()
    return _key_string_set(source, keys, value, mode)

def _key_string_set(source, keys, value, mode):
    key = keys.pop()
    try: key = int(key) 
    except:
        if len(key)==0:
            key=max(map(lambda o: o if type(o)==int else -1, source.keys()) or [-1])+1
    if len( keys ):
        if key in source:
            if not isinstance( source.get(key), dict ):
                if mode & STRICT == STRICT:
                    raise KeyError()
                source[key] = {}
            _key_string_set(source[key], keys, value, mode)
        else:
            source[key] = {}
            _key_string_set(source[key], keys, value, mode)
    else:
        source[key] = value
