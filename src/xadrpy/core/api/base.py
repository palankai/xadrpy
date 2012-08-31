import logging
import conf
from django.conf import settings
from xadrpy.core.api.exceptions import IllegalWrapperOption, IllegalServiceOption

logger = logging.getLogger("xadrpy.api.core.base")

class Services(object):

    def __init__(self, namespace, store):
        self.namespace = namespace
        self.store = store

    def register(self, func=None, name=None, **options):
        def inner(func):
            wrappers = options.get('wrappers', False)
            func = self._apply_wrappers(func, wrappers)

            self.add(func, name or func.__name__, options)
            return func
        if func:
            return inner(func)
        else:
            return inner

    def _apply_wrappers(self, func, wrappers):
        if wrappers == False:
            return func
        if callable(wrappers): wrappers = (wrappers,)
        if isinstance(wrappers, (list, tuple)):
            for wrapper in wrappers:
                func = wrapper(func)
            return func
        raise IllegalServiceOption("Illegal wrapper option for %s.%s" % (func.__module__, func.__name__))

    def add(self, service, name, options):
        self.store[(self.namespace, name)] = (service, options, self)
        logger.debug("Register: %s.%s with %s", self.namespace, name, options)


class HttpServices(Services):

    def __init__(self, namespace=None, error_status=200):
        Services.__init__(self, namespace, conf.HTTP_SERVICES)
        self.error_status = 200

    def register(self, func=None, name=None, args=(), **options):
        options.setdefault("args", args)
        return Services.register(self, func, name, **options)
