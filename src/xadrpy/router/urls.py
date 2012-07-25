from django.conf.urls import patterns, include, url
from models import Route
from django.conf import settings

if 'xadrpy.contrib.feedback' in settings.INSTALLED_APPS:
    urlpatterns = patterns("",
        url('^feedback/', include('xadrpy.contrib.feedback.urls'))
        )
else:
    urlpatterns = patterns("")

def append_database_urls(urlpatterns):
    for route in Route.objects.all():
        route.append_pattern(urlpatterns)

append_database_urls(urlpatterns)