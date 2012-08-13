from django.utils import translation
from django.middleware.locale import LocaleMiddleware
import conf
from django.conf import settings

class LocaleMiddleware(LocaleMiddleware):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_kwargs:
            LANGUAGE_CODE = view_kwargs.pop(conf.LANGUAGE_CODE_KWARG,settings.LANGUAGE_CODE)
            translation.activate(LANGUAGE_CODE)
            request.LANGUAGE_CODE = LANGUAGE_CODE
