from libs import MetaHandler
from base import Application
import logging
from django.dispatch.dispatcher import receiver
from xadrpy.utils.signals import autodiscover_signal

__all__ = ["MetaHandler", "Application"]

logger = logging.getLogger("xadrpy.core.router")

@receiver(autodiscover_signal, dispatch_uid="init_meta_handler")
def init_meta_handler(**kwargs):
    import conf
    from django.conf import settings
    from xadrpy.utils.imports import get_installed_apps_module, get_class
    
    for conf_module in get_installed_apps_module("conf"):
        conf.META_HANDLER = getattr(conf_module, "META_HANDLER", conf.META_HANDLER)
    conf.META_HANDLER = getattr(settings, "META_HANDLER", conf.META_HANDLER)
    conf.META_HANDLER_CLS = get_class(conf.META_HANDLER)
