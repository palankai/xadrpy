from django.conf.urls import patterns
from models import Route

urlpatterns = patterns("")

def append_database_urls(urlpatterns):
    for route in Route.objects.all():
        route.append_pattern(urlpatterns)

append_database_urls(urlpatterns)