from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import copy

class BaseResolver(object):
    def __init__(self, column):
        self.column = column
    
    def get_urls(self, kwargs={}):
        kwargs.update({'route': self.column})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [
            url(self.column.get_translated_regex(slash=slash), self.column.get_view_name(), kwargs=kwargs, name=self.column.name),
            url(self.column.get_translated_regex(postfix='(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.blog.views.post', kwargs=kwargs, name=self.column.name)
        ]
    
    def get_absolute_url(self, post):
        return reverse('xadrpy.contrib.blog.views.post', kwargs={'slug': post.slug})   
        

class MonthBasedResolver(BaseResolver):

    def get_urls(self, kwargs={}):
        kwargs.update({'route': self.column})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        year_kwargs = copy.copy(kwargs)
        month_kwargs = copy.copy(kwargs)
        year_kwargs.update({'title': _("Post's from %(publication__year)s")})
        month_kwargs.update({'title': _("Post's from %(publication__year)s-%(publication__month)s")})
        return [
            url(self.column.get_translated_regex(), self.column.get_view_name(), kwargs=kwargs, name=self.column.name),
            url(self.column.get_translated_regex(postfix='(?P<publication__year>[0-9]{4})/$'), 'xadrpy.contrib.blog.views.posts', kwargs=year_kwargs, name=self.column.name),
            url(self.column.get_translated_regex(postfix='(?P<publication__year>[0-9]{4})/(?P<publication__month>[0-9]{2})/$'), 'xadrpy.contrib.blog.views.posts', kwargs=month_kwargs, name=self.column.name),
            url(self.column.get_translated_regex(postfix='(?P<publication__year>[0-9]{4})/(?P<publication__month>[0-9]{2})/(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.blog.views.post', kwargs=kwargs, name=self.column.name),
        ]

    def get_absolute_url(self, post):
        year = post.created.year
        month = post.created.strftime("%m")
        return reverse('xadrpy.contrib.blog.views.post', kwargs={'slug': post.slug, 'publication__year': year, 'publication__month': month})   
