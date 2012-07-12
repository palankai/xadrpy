from django.db import models
from django.contrib.sites.models import Site
from xadrpy.models.fields.nullchar_field import NullCharField
from xadrpy.models.inheritable import TreeInheritable
import conf
from xadrpy.models.fields.dict_field import DictField
from django.utils.translation import ugettext_lazy as _, get_language
from django.conf.urls import patterns, include, url
from django.utils.functional import lazy
from xadrpy.i18n.utils import i18n_patterns
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
import os
import hashlib
import xadrpy

class Route(TreeInheritable):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=conf.DEFAULT_SITE_ID)
    language_code = NullCharField(max_length=5, verbose_name=_("Language code"))
    slug = NullCharField(max_length=255, verbose_name=_("URL part"))
    meta = DictField(verbose_name=_("Meta data"))
    i18n = models.BooleanField(default=False)
    signature = NullCharField(max_length=128)
    
    need_reload = True
    
    class Meta:
        unique_together = ('site', 'language_code', 'parent', 'slug')
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        db_table = "xadrpy_router_route"
    
    def get_regex(self, postfix="$", slash="/", language_code=None):
        root_language_code = self.get_root_language_code()
        if not self.parent:
            regex = root_language_code and "^%s/" % root_language_code or "^"
        else:
            regex = self.parent.get_regex(postfix="", slash="/", language_code=language_code)
        slug = self.get_slug(language_code)
        if slug:
            slug = slug+slash
        regex += slug 
        return regex + postfix

    def get_slug(self, language_code):
        try:
            alternative = self.alternatives.get(site=self.site, language_code=language_code)
            return alternative.slug
        except: 
            pass
        return self.slug or ""

    def get_translated_regex(self, postfix="$", slash="/"):
        language_code = get_language()
        return self.get_regex(postfix=postfix, slash=slash, language_code=language_code)
    
    get_translated_regex = lazy(get_translated_regex, unicode)
    
    def __unicode__(self):
        return self.get_regex()
    
    def patterns(self, *args, **kwargs):
        if not self.parent and self.i18n:
            return i18n_patterns(*args, **kwargs)
        return patterns(*args, **kwargs)
    
    def get_urls(self, kwargs={}):
        return []
    
    def append_pattern(self, url_patterns):
        root_language_code = self.get_root_language_code()
        kwargs = root_language_code and {conf.LANGUAGE_CODE_KWARG: root_language_code} or {}
        urls = self.get_urls(kwargs)
        if not urls: return
        url_patterns+=self.patterns('', *urls)
    
    def get_root_language_code(self):
        return self.get_root().language_code
    
    def get_signature(self):
        return u"%s:%s-%s-%s-%s" % (xadrpy.VERSION, self.site.id, not self.parent and self.language_code or None, self.slug, self.i18n)

@receiver(pre_save, sender=None)
def check_signature(sender, instance, **kwargs):
    if isinstance(instance, Route):
        signature = hashlib.md5(instance.signature).hexdigest()
        instance.signature_changed = instance.get_signature() != signature
        if instance.signature_changed:
            instance.signature = signature
            instance.signature_changed = instance.need_reload and conf.WSGI_PATH
    
if conf.TOUCH_WSGI_FILE:
    @receiver(post_save, sender=None)
    def touch_wsgi_file(sender, instance, **kwargs):
        if isinstance(instance, Route) and instance.need_reload and conf.WSGI_PATH:
            with file(conf.WSGI_PATH, 'a'):
                os.utime(conf.WSGI_PATH, None)

class RouteAlternatives(models.Model):
    route = models.ForeignKey(Route, verbose_name=_("Route"), related_name="alternatives")
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=conf.DEFAULT_SITE_ID)
    language_code = NullCharField(max_length=5, verbose_name=_("Language code"))
    slug = NullCharField(max_length=255, verbose_name=_("URL part"))
    meta = DictField(verbose_name=_("Meta data"))

    class Meta:
        unique_together = ('route', 'site', 'language_code')
        verbose_name = _("Route alternative")
        verbose_name_plural = _("Route alternatives")
        db_table = "xadrpy_router_route_alternatives"

class View(Route):
    view_name = models.CharField(max_length=255)
    kwargs = DictField()
    name = NullCharField(max_length=255)
    
    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")
        db_table = "xadrpy_router_view"

    def get_urls(self, kwargs={}):
        kwargs.update(self.kwargs or {})
        return [url(self.get_translated_regex(), self.view_name, kwargs=kwargs, name=self.name)]

class Include(Route):
    include_name = models.CharField(max_length=255)
    namespace = NullCharField(max_length=255)
    app_name = NullCharField(max_length=255)
    kwargs = DictField()

    class Meta:
        verbose_name = _("Include")
        verbose_name_plural = _("Includes")
        db_table = "xadrpy_router_include"

    def get_urls(self, kwargs={}):
        kwargs.update(self.kwargs or {})
        return url(self.get_translated_regex(postfix=""), include(self.include_name, self.namespace, self.app_name), kwargs=kwargs)

class Static(Route):
    path = models.FilePathField(max_length=255, verbose_name=_("Path"))
    mimetype = NullCharField(max_length=255, verbose_name=_("Mime type"))

    class Meta:
        verbose_name = _("Static")
        verbose_name_plural = _("Statics")
        db_table = "xadrpy_router_static"

    def get_regex(self, postfix="$", slash="/"):
        return super(Static, self).get_regex(postfix=postfix, slash="")

    def get_urls(self, kwargs={}):
        kwargs.update({'router': self})
        return [url(self.get_translated_regex(), 'xadrpy.routers.views.static', kwargs=kwargs)]        

class Template(Route):
    template_name = models.CharField(max_length=255, verbose_name=_("Template name"))
    mimetype = NullCharField(max_length=255, verbose_name=_("Mime type"))
    context = DictField()

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        db_table = "xadrpy_router_template"

    def get_regex(self, postfix="$", slash="/"):
        return super(Static, self).get_regex(postfix=postfix, slash="")

    def get_urls(self, kwargs={}):
        kwargs.update({'router': self})
        return [url(self.get_translated_regex(), 'xadrpy.routers.views.template', kwargs=kwargs)]

class InlineTemplate(Route):
    body = models.TextField(verbose_name=_("Template"))
    mimetype = NullCharField(max_length=255, verbose_name=_("Mime type"))
    context = DictField()

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        db_table = "xadrpy_router_inline_template"

    def get_regex(self, postfix="$", slash="/"):
        return super(Static, self).get_regex(postfix=postfix, slash="")
    
    def get_urls(self, kwargs={}):
        kwargs.update({'router': self})
        return [url(self.get_translated_regex(), 'xadrpy.routers.views.inline_template', kwargs=kwargs)]
    
class Redirect(Route):
    url = NullCharField(max_length=255, null=False, blank=False, verbose_name=_("URL"))
    permanent = models.BooleanField(default=False, verbose_name=_("Permanent"))

    class Meta:
        verbose_name = _("Redirect")
        verbose_name_plural = _("Redirects")
        db_table = "xadrpy_router_redirect"

    def get_urls(self, kwargs={}):
        kwargs.update({'router': self})
        return [url(self.get_translated_regex(), 'xadrpy.routers.views.redirect', kwargs=kwargs)] 
