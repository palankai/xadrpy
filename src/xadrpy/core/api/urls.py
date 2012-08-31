from django.conf.urls.defaults import patterns, url, include
import logging

logger = logging.getLogger("API")


urlpatterns = patterns('',
    url(r'^$', 'xadrpy.core.api.views.home', name="APIBASE"),
    url(r'^auth/get_permissions/$', 'xadrpy.core.api.views.get_permissions'),
    url(r'^(?P<namespace>[a-zA-Z0-9_\.\-]+)/(?P<name>[a-zA-Z0-9_\.\-]+)/$', 'xadrpy.core.api.views.serve', name="API-Serve"),
    url(r'^(?P<name>[a-zA-Z0-9_\.\-]+)/$', 'xadrpy.core.api.views.serve', name="API-Serve"),
)
