from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sandbox.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns( '',
       ( r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip( "/" ), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
   )
