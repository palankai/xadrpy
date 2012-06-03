from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/filebrowser/', include(site.urls)),    
    url(r'^admin/rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    
    url(r'^$', '{{ project_name }}.views.home', name='home'),
)
