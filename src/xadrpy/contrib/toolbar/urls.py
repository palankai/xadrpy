from django.conf.urls import patterns, url

urlpatterns = patterns('xadrpy.contrib.toolbar.views',
    url('^$', 'toolbar'),
    url('^switch/(?P<key>[0-9a-zA-Z\-_\.]+)/$', 'switch')
)