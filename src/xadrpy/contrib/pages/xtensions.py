from xadrpy.router.base import Application
from django.conf import settings
from django.conf.urls import url
import conf

class PageApplication(Application):

    def get_urls(self, kwargs={}):
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [url(self.route.get_translated_regex(slash=slash), conf.DEFAULT_VIEW, kwargs=kwargs, name=self.route.name)]
