from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),    
    url(r'^(?P<content_type_id>[\d]+)/(?P<object_id>[\d]+)/$', 'xadrpy.contrib.feedback.views.receive_trackback', name="receive_trackback"),
    #url(r'^xml-rpc/$', 'xadrpy.vendor.trackback.views.receive_pingback', {}, name="receive_pingback"),
)