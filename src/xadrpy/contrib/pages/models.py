from django.db import models
from django.utils.translation import ugettext_lazy as _
from xadrpy.models.fields.nullchar_field import NullCharField
import conf
import datetime
from xadrpy.router.models import Route, ViewRoute
from xadrpy.models.fields.dict_field import DictField
from xadrpy.models.fields.json_field import JSONField
from xadrpy.models.inheritable import Inheritable, TreeInheritable
from ckeditor.fields import RichTextField
import logging
from xadrpy.auth.models import OwnedModel
from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404
from django.core.urlresolvers import reverse

logger = logging.getLogger("Pages")

class Page(ViewRoute, OwnedModel):
    is_layout = models.BooleanField(default=False)
    layout = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Layout"), related_name="+")
    template_name = models.CharField(max_length=255, blank=True, null=True, choices=conf.TEMPLATES, verbose_name = _("Template"))
    extra_classes = models.CharField(max_length=255, blank=True, verbose_name = _("Extra classes"), default="")
    enable_comments = models.BooleanField(default=True, verbose_name = _("Enable comments"), db_index=True)

    status = models.CharField(max_length=16, choices=conf.PAGE_STATES, default='PUB')
    publication = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    publication_end = models.DateTimeField(verbose_name = _("Publication end"), null=True, blank=True, db_index=True)

    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        db_table = "xadrpy_pages_page"

    def get_view_name(self):
        return self.view_name or conf.DEFAULT_VIEW

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
            return layout.template_name or conf.DEFAULT_TEMPLATE 
        return conf.DEFAULT_TEMPLATE

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

class PluginInstance(TreeInheritable, OwnedModel):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))

    plugin = models.CharField(max_length=255)

    page = models.ForeignKey(Page, null=True)
    placeholder = NullCharField(max_length=255)
    position = models.IntegerField(default=1)

    language_code = NullCharField(max_length=5)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Plugin")
        verbose_name_plural = _("Plugins")
        db_table = "xadrpy_pages_plugin_instance"
    
    def __unicode__(self):
        return self.key
