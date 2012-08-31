from django.dispatch.dispatcher import receiver
from xadrpy.utils.signals import autodiscover_signal

@receiver(autodiscover_signal, dispatch_uid="api_autodiscover")
def api_autodiscover(**kwargs):
    import imp
    import conf
    from django.conf import settings
    from django.utils import importlib
    from django.conf.urls import url
    from urls import urlpatterns

    for app in settings.INSTALLED_APPS:

        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('api', app_path)
        except ImportError:
            continue
        module = importlib.import_module("%s.api" % app)
        #module_name = getattr(module, "API_MODULE_NAME", app)

    for pattern, method, kwargs in conf.urls:
        urlpatterns.append(url(pattern, method, kwargs=kwargs))
