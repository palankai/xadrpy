VERSION = (0,6,0,"alpha",0)

def autodiscover():
    import logging
    from xadrpy.utils.signals import autodiscover_signal
    from xadrpy.utils.imports import get_installed_apps_module
    from django.conf import settings
    from django.utils.importlib import import_module
    logger = logging.getLogger("xadrpy.autodiscover")
    
    for xtensions in get_installed_apps_module("xtensions"):
        logger.debug("%s loaded.", xtensions.__name__)
    if hasattr(settings, "XTENSIONS"):
        xtensions = import_module(getattr(settings, "XTENSIONS"))
        logger.debug("%s loaded.", xtensions.__name__)

    for receiver, response in autodiscover_signal.send_robust(None):
        name = "%s.%s(%s)" % (receiver.__module__, receiver.__name__, ", ".join(receiver.__code__.co_varnames[:receiver.__code__.co_argcount]))
        if isinstance(response, Exception):
            exception_name = "%s.%s" % (response.__class__.__module__,response.__class__.__name__)
            logger.error("%s ERROR: %s(%s)", name, exception_name , response)
        else:
            logger.debug("%s success", name)
    
def get_version():
    from utils.version import get_version
    return get_version(VERSION)
