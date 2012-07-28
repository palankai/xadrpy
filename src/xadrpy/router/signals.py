from django.dispatch.dispatcher import Signal

prepend_route_urls = Signal(providing_args=['urlpatterns'])
append_route_urls = Signal(providing_args=['urlpatterns'])