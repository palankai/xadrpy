from conf import CONTAINERS
from xadrpy.core.workers.exceptions import InvalidContainerName

def load_container_classes():
    containers = []
    for container_name, container_class_name in CONTAINERS:
        containers.append((container_name, get_container_class(container_class_name)))
    return containers
        
def get_container_class(name):
    import sys, types
    parts = name.split(".")
    parent = parts.pop(0)
    while len(parts):
        if not parent in sys.modules:
            __import__(parent)
        cls = sys.modules[parent]
        part = parts.pop(0)
        if getattr(cls, part,None) and type(getattr(cls, part))!=types.ModuleType:
            break
        parent+="."+part
    while len(parts):
        cls = getattr(cls, part)
        part = parts.pop(0)
    try:
        cls = getattr(cls, part)
    except AttributeError:
        raise InvalidContainerName(name)
    return cls        