from django.db import models
from django.utils.translation import ugettext_lazy as _
from xadrpy.models.fields.nullchar_field import NullCharField
import conf
import datetime
from xadrpy.router.models import ViewRoute
from xadrpy.models.inheritable import TreeInheritable
from ckeditor.fields import RichTextField
import logging
from xadrpy.access.models import OwnedModel
from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse, get_resolver, NoReverseMatch,\
    Resolver404
from xadrpy.models.fields.stringset_field import StringSetField
from xadrpy.utils.signals import autodisvover_signal
from django.dispatch.dispatcher import receiver
from xadrpy.contrib.pages.libs import Plugin, PLUGIN_CACHE
from xadrpy.vendor import trackback
from inspect import isclass
from django.contrib.sites.models import Site

logger = logging.getLogger("Pages")

class Page(ViewRoute, OwnedModel):
    is_layout = models.BooleanField(default=False)
    layout = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Layout"), related_name="+")
    template_name = models.CharField(max_length=255, blank=True, null=True, choices=conf.TEMPLATES, verbose_name = _("Template"))
    extra_classes = models.CharField(max_length=255, blank=True, verbose_name = _("Extra classes"), default="")
    enable_comments = models.BooleanField(default=True, verbose_name = _("Enable comments"), db_index=True)
    lock_comments = models.BooleanField(default=False, verbose_name = _("Lock comments"), db_index=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View count"))

    status = models.CharField(max_length=16, choices=conf.PAGE_STATES, default='PUB')
    publication = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    publication_end = models.DateTimeField(verbose_name = _("Publication end"), null=True, blank=True, db_index=True)

    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))
    
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta title"))
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta keywords"))
    meta_description = models.TextField(blank=True, null=True, verbose_name=_("Meta description"))
    meta_robots = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta robots"))
    meta_cannonical = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta cannoncical"))

    default_view = None
    default_template = None

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        db_table = "xadrpy_pages_page"

    def get_view_name(self):
        return self.view_name or self.default_view or conf.DEFAULT_VIEW

    def get_urls(self, kwargs={}):
        kwargs.update({'route': self})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [url(self.get_translated_regex(slash=slash), self.get_view_name(), kwargs=kwargs, name=self.name)]
    
    def get_layout(self):
        if self.layout:
            return self.layout
        if isinstance(self.get_parent(), Page):
            return self.get_parent().get_layout()
        else:
            return None
    
    def get_template(self):
        layout = self.get_layout()
        if layout:
            return layout.template_name or layout.default_template or conf.DEFAULT_TEMPLATE 
        return self.default_template or conf.DEFAULT_TEMPLATE

    def get_absolute_url(self):
        return reverse(self.get_view_name(), kwargs={'route': self})
    
    def can_render(self):
        if datetime.datetime.now().replace(tzinfo=None) < self.publication.replace(tzinfo=None):
            return False
        if self.publication_end and datetime.datetime.now().replace(tzinfo=None) > self.publication_end.replace(tzinfo=None):
            return False
        if self.status == 'DRA':
            return False
        return True    
    
    def render_to_response(self, request, context={}):
        layout = self.get_layout()
        template = self.get_template()
        
        context.update({
            'page': self,
            'layout': layout
        })
        return render_to_response(template, context, RequestContext(request))
    
    def resolve(self, args, kwargs):
        return self

    def get_meta_title(self):
        parent_title = ""
        self_title = self.meta_title or self.title 
        if self.get_parent() and self.get_parent().get_meta_title():
            self_title = self_title + " | " + self.get_parent().get_meta_title()
        return self_title


class PluginStore(models.Model):
    plugin = models.CharField(max_length=255, unique=True)
    template = NullCharField(max_length=255)
    slots = StringSetField()

    class Meta:
        verbose_name = _("Plugin store")
        verbose_name_plural = _("Plugin store")
        db_table = "xadrpy_pages_plugin_store"

@receiver(autodisvover_signal)
def register_in_store(**kwargs):
    import imp
    from django.utils import importlib

    for app in settings.INSTALLED_APPS:
        
        try:                                                                                                                          
            app_path = importlib.import_module(app).__path__                                                                          
        except AttributeError:                                                                                                        
            continue 
        
        try:                                                                                                                          
            imp.find_module('plugins', app_path)                                                                               
        except ImportError:                                                                                                           
            continue                                                                                                                  
        module = importlib.import_module("%s.plugins" % app)
        for name in dir(module):
            cls = getattr(module,name)
            if isclass(cls) and issubclass(cls, Plugin) and cls!=Plugin:
                store = PluginStore.objects.get_or_create(plugin=cls.get_name())[0]
                if store.template:
                    cls.template = store.template
                PLUGIN_CACHE[cls.get_name()]=cls
                if cls.alias:
                    PLUGIN_CACHE[cls.alias]=cls

class PluginInstance(TreeInheritable, OwnedModel):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))

    plugin = models.CharField(max_length=255)
    placeholder = NullCharField(max_length=255)

    page = models.ForeignKey(Page, null=True)
    position = models.IntegerField(default=1)

    language_code = NullCharField(max_length=5)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Plugin")
        verbose_name_plural = _("Plugins")
        db_table = "xadrpy_pages_plugin_instance"
    
    def __unicode__(self):
        return self.key

class SnippetInstance(PluginInstance):
    body = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Snippet Plugin")
        verbose_name_plural = _("Snippet Plugins")
        db_table = "xadrpy_pages_snippet_instance"

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