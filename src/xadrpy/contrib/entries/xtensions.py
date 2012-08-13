from xadrpy.core.router.base import Application
from django.db.models import permalink
from django.conf import settings
from django.conf.urls import url
from xadrpy.contrib.entries.feeds import ColumnEntriesFeed
import copy
from django.utils.translation import ugettext_lazy as _


class EntriesApplication(Application):

    @permalink
    def get_absolute_url(self):
        return ("xadrpy.contrib.entries.views.column", (),{'route_id': self.route.id})

class SimpleEntriesApplication(EntriesApplication):

    def get_urls(self, kwargs={}):
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [
            url(self.get_translated_regex(slash=slash), "xadrpy.contrib.entries.views.column", kwargs=kwargs, name=self.route.name),
            url(self.get_translated_regex(postfix='rss/$'), ColumnEntriesFeed(self.route)),
            url(self.get_translated_regex(postfix='(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.entries.views.entry', kwargs=kwargs, name=self.route.name)
        ]
    
    @permalink
    def get_entry_absolute_url(self, entry):
        return (self.route.name or 'xadrpy.contrib.entries.views.entry', (), {'slug': entry.slug})

class MonthBasedEntriesApplication(EntriesApplication):

    def get_urls(self, kwargs={}):
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        year_kwargs = copy.copy(kwargs)
        month_kwargs = copy.copy(kwargs)
        year_kwargs.update({'title': _("Entries from %(pub_date__year)s")})
        month_kwargs.update({'title': _("Entries from %(pub_date__year)s-%(pub_date__month)s")})
        return [
            url(self.get_translated_regex(), "xadrpy.contrib.entries.views.column", kwargs=kwargs, name=self.route.name),
            url(self.get_translated_regex(postfix='rss/$'), ColumnEntriesFeed(self.route)),
            url(self.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/$'), 'xadrpy.contrib.entries.views.posts', kwargs=year_kwargs, name=self.route.name),
            url(self.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/(?P<pub_date__month>[0-9]{2})/$'), 'xadrpy.contrib.entries.views.posts', kwargs=month_kwargs, name=self.route.name),
            url(self.get_translated_regex(postfix='(?P<pub_date__year>[0-9]{4})/(?P<pub_date__month>[0-9]{2})/(?P<slug>[0-9a-zA-Z\-/_]+)'+slash+"$"), 'xadrpy.contrib.entries.views.entry', kwargs=kwargs, name=self.route.name),
        ]

    @permalink
    def get_entry_absolute_url(self, entry):
        year = entry.pub_date.year
        month = entry.pub_date.strftime("%m")
        return (self.route.name or 'xadrpy.contrib.entries.views.entry', (), {'slug': entry.slug, 'pub_date__year': year, 'pub_date__month': month})
       