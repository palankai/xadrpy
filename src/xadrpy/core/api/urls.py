from django.conf.urls.defaults import patterns, url, include
import logging

logger = logging.getLogger("API")


urlpatterns = patterns('',
    url(r'^$', 'xadrpy.core.api.views.home', name="APIBASE"),
    url(r'^auth/get_permissions/$', 'xadrpy.core.api.views.get_permissions')
)
