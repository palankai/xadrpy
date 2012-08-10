from django.utils.functional import memoize
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
import imp

_loaded_classes = SortedDict()


def _get_class(import_path, base_class=object):

    module, attr = import_path.rsplit('.', 1)

    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))
    if base_class and not issubclass(cls, base_class):
        raise ImproperlyConfigured('Class "%s" is not a subclass of "%s"' %
                                   (cls, base_class))
    return cls
get_class = memoize(_get_class, cache=_loaded_classes, num_args=1)

def get_installed_apps_module(name):
    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue
        try:
            imp.find_module(name, app_path)
        except ImportError:
            continue
        module_name = "%s.%s" % ( app, name )
        module = import_module(module_name)
        yield module
