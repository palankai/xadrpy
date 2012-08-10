from django.db import models
from django.utils.translation import ugettext_lazy as _
import conf
import datetime
from xadrpy.router.models import RouteTranslation, Route
from ckeditor.fields import RichTextField
import logging
from xadrpy.access.models import OwnedModel
from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse, get_resolver, NoReverseMatch,\
    Resolver404
from xadrpy.vendor import trackback
from django.contrib.sites.models import Site
from django.http import Http404
from xadrpy.contrib.pages.xtensions import PageApplication

logger = logging.getLogger("Pages")

class Page(Route, OwnedModel):
    comments_enabled = models.BooleanField(default=False, verbose_name = _("Comments enabled"), db_index=True)
    comments_unlocked = models.BooleanField(default=False, verbose_name = _("Comments locked"), db_index=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View count"))

    published = models.BooleanField(default=True, verbose_name=_("Is published"))
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication date"), db_index=True)

    show_content = models.BooleanField(default=True, verbose_name=_("Visible content"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        db_table = "xadrpy_pages_page"

    def get_view_name(self):
        return conf.DEFAULT_VIEW

    def get_application_class(self):
        return PageApplication 

    def get_content_pages(self):
        return conf.PAGE_BREAK_RE.split(self.content) 

    def get_content(self):
        return "".join(self.get_content_pages())

    def get_content_tail(self):
        return "".join(self.get_content_pages())[1:]

    def get_content_head(self):
        return "".join(self.get_content_pages())[0]
    
    def get_template(self):
        return conf.DEFAULT_TEMPLATE

    def get_absolute_url(self):
        if self.app and hasattr(self.app, "get_absolute_url"):
            return self.app.get_absolute_url()
        return reverse(self.get_view_name(), kwargs={'route_id': self.id})
    
    def can_render(self):
        if not self.enabled or not self.published:
            return False 
        if datetime.datetime.now().replace(tzinfo=None) < self.pub_date.replace(tzinfo=None):
            return False
        return True    
    
    def resolve(self, args, kwargs):
        return self
    
    def get_context(self, request, args=(), kwargs={}):
        return dict(super(Page, self).get_context(request, args, kwargs), **{
            'content': self.get_content(),
            'content_title': self.get_title(),
            'show_content': self.show_content,
        })
    
    def increment_view_count(self, request):
        if request.user.is_staff or self.user == request.user: return
        self.view_count = models.F("view_count")+1
        self.save()
        


class PageTranslation(RouteTranslation):
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    class Meta:
        db_table = "xadrpy_pages_page_translation"

PageTranslation.register(Page)



def resolver(target_url):
    try:
        urlresolver = get_resolver(None)
        site = Site.objects.get_current()
        func, args, kwargs = urlresolver.resolve(target_url.replace("http://%s"%site.domain, ''))
        route = kwargs.pop("route", None)
        if route:
            return route.resolve(args, kwargs)
    except (NoReverseMatch, Resolver404), e:
        return None        
            
trackback.registry.add(resolver)