from django.conf.urls import patterns, include, url
from models import Route
from django.conf import settings
import signals

if 'xadrpy.contrib.feedback' in settings.INSTALLED_APPS:
    urlpatterns = patterns("",
        url('^feedback/', include('xadrpy.contrib.feedback.urls'))
        )
else:
    urlpatterns = patterns("")

def append_database_urls(urlpatterns):
    signals.prepend_route_urls.send(None, urlpatterns=urlpatterns)
    for route in Route.objects.all():
        route.append_pattern(urlpatterns)
    signals.append_route_urls.send(None, urlpatterns=urlpatterns)

append_database_urls(urlpatterns)