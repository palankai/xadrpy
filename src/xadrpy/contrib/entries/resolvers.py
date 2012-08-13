from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import copy
from feeds import ColumnEntriesFeed

class BaseResolver(object):
    def __init__(self, column):
        self.column = column
    
    def get_urls(self, kwargs={}):
        #kwargs.update({'route_id': self.column.id})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [
            url(self.column.app.get_translated_regex(slash=slash), self.column.get_view_name(), kwargs=kwargs, name=self.column.name),
            url(self.column.app.get_translated_regex(postfix='rss/$'), ColumnEntriesFeed(self.column)),
            url(self.column.app.get_translated_regex(postfix='(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.entries.views.entry', kwargs=kwargs, name=self.column.name)
        ]
    
    def get_absolute_url(self, entry):
        view_name = self.column.name or 'xadrpy.contrib.blog.views.entry'
        return reverse(view_name, kwargs={'slug': entry.slug})   
        

class MonthBasedResolver(BaseResolver):

    def get_urls(self, kwargs={}):
        #kwargs.update({'route_id': self.column.id})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        year_kwargs = copy.copy(kwargs)
        month_kwargs = copy.copy(kwargs)
        year_kwargs.update({'title': _("Entries from %(pub_date__year)s")})
        month_kwargs.update({'title': _("Entries from %(pub_date__year)s-%(pub_date__month)s")})
        return [
            url(self.column.app.get_translated_regex(), self.column.get_view_name(), kwargs=kwargs, name=self.column.name),
            url(self.column.app.get_translated_regex(postfix='rss/$'), ColumnEntriesFeed(self.column)),
            url(self.column.app.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/$'), 'xadrpy.contrib.entries.views.posts', kwargs=year_kwargs, name=self.column.name),
            url(self.column.app.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/(?P<pub_date__month>[0-9]{2})/$'), 'xadrpy.contrib.entries.views.posts', kwargs=month_kwargs, name=self.column.name),
            url(self.column.app.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/(?P<pub_date__month>[0-9]{2})/(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.entries.views.entry', kwargs=kwargs, name=self.column.name),
        ]

    def get_absolute_url(self, entry):
        view_name = self.column.name or 'xadrpy.contrib.entries.views.entry'
        year = entry.pub_date.year
        month = entry.pub_date.strftime("%m")
        return reverse(view_name, kwargs={'slug': entry.slug, 'pub_date__year': year, 'pub_date__month': month})   
