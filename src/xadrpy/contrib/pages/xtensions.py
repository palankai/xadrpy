from xadrpy.core.router.base import Application
from django.conf import settings
from django.conf.urls import url
import conf
from django.db.models import permalink

class PageApplication(Application):

    @permalink
    def get_absolute_url(self):
        return (conf.DEFAULT_VIEW, (),{'route_id': self.route.id})

    def get_urls(self, kwargs={}):
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [url(self.get_translated_regex(slash=slash), conf.DEFAULT_VIEW, kwargs=kwargs, name=self.route.name)]
