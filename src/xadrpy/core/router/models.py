from django.db import models
from django.contrib.sites.models import Site
from xadrpy.core.models.fields.nullchar_field import NullCharField
from xadrpy.core.models.inheritable import TreeInheritable
import conf
from django.utils.translation import ugettext_lazy as _
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
import os
import hashlib
from xadrpy.core.i18n.models import Translation
from xadrpy.core.i18n.fields import TranslationForeignKey
from xadrpy.core.models.fields.dict_field import DictField
from xadrpy.core.models.fields.language_code_field import LanguageCodeField
import logging
import base
import xtensions
from xadrpy.core.models.fields.class_field import ClassNameField
from xadrpy.core.preferences.fields import PrefsStoreField
from xadrpy.core.router.base import get_local_request

logger = logging.getLogger("xadrpy.router.models")

class Route(TreeInheritable):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    master = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Master"), related_name="+")
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=conf.DEFAULT_SITE_ID)
    language_code = LanguageCodeField(verbose_name=_("Language code"), blank=True, null=True, default=None)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="images", blank=True, null=True, verbose_name = _("Image"))
    slug = NullCharField(max_length=255, verbose_name=_("URL part"))
    i18n = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True, verbose_name=_("Is enabled"))
    visible = models.BooleanField(default=True, verbose_name=_("Is visible"))
    signature = NullCharField(max_length=128, editable=False, default="")
    name = NullCharField(max_length=255, unique=True)
    application_name = ClassNameField("app", max_length=128, verbose_name=_("Application name"), fallback="get_application_class")
    meta = PrefsStoreField("prefs", fallback="get_prefs_class")
    
    need_reload = True
    
    class Meta:
        unique_together = ('site', 'language_code', 'parent', 'slug')
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        db_table = "xadrpy_router_route"

    def __unicode__(self):
        return self.title
    
    def get_application_class(self):
        return base.Application

    def get_application_choices(self):
        class_name = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        if class_name in conf.APPLICATIONS:
            return conf.APPLICATIONS[class_name]

    def get_prefs_class(self):
        return base.RoutePrefs
    
    def get_absolute_url(self):
        return self.app.get_absolute_url()
    
    def get_title(self):
        return self.translation().title

    def get_slug(self, language_code):
        return self.translation(language_code=language_code).slug or self.slug or ""
    
    def get_master(self):
        if hasattr(self, "_master"):
            return self._master
        if self.master: 
            self._master = self.master.descendant
        elif self.get_parent(): 
            self._master = self.get_parent().get_master()
        else:
            self._master = None 
        return self._master
    
    
    def get_meta(self):
        return conf.META_HANDLER_CLS(self)
    
    def get_signature(self):
        return u"%s:%s-%s-%s-%s-%s-%s" % (conf.VERSION, self.site.id, not self.parent and self.language_code or None, self.slug, not self.parent and self.i18n, self.enabled, self.application_name)

    def save( self, *args, **kwargs ):
        signature = hashlib.md5(self.get_signature()).hexdigest()
        if self.signature != signature:
            logger.info("Route (#%s) signature changed", self.id)
            self.signature = signature
            setattr(conf._local, "need_wsgi_reload", True)
        TreeInheritable.save(self, *args, **kwargs)


class RouteTranslation(Translation):
    origin = TranslationForeignKey(Route, related_name="+")
    language_code = LanguageCodeField()

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="images", blank=True, null=True, verbose_name = _("Image"))
    slug = NullCharField(max_length=255, verbose_name=_("URL part"))
    meta = DictField(default={})

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta title"))
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta keywords"))
    meta_description = models.TextField(blank=True, null=True, verbose_name=_("Meta description"))

    class Meta:
        db_table = "xadrpy_router_route_translation"

RouteTranslation.register(Route)

class IncludeRoute(Route):
    include_name = models.CharField(max_length=255)
    namespace = NullCharField(max_length=255)

    class Meta:
        verbose_name = _("Include")
        verbose_name_plural = _("Includes")
        db_table = "xadrpy_router_include"
    
    def get_application_class(self):
        return xtensions.IncludeApplication

class StaticRoute(Route):
    path = models.FilePathField(max_length=255, verbose_name=_("Path"))
    mimetype = NullCharField(max_length=255, verbose_name=_("Mime type"))

    class Meta:
        verbose_name = _("Static")
        verbose_name_plural = _("Statics")
        db_table = "xadrpy_router_static"

    def get_regex(self, postfix="$", slash="/"):
        return super(StaticRoute, self).get_regex(postfix=postfix, slash="")

    def get_application_class(self):
        return xtensions.StaticApplication


class TemplateRoute(Route):
    template_name = models.CharField(max_length=255, verbose_name=_("Template name"))
    mimetype = NullCharField(max_length=255, verbose_name=_("Mime type"))

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        db_table = "xadrpy_router_template"

    def get_regex(self, postfix="$", slash="/"):
        return super(TemplateRoute, self).get_regex(postfix=postfix, slash="")

    def get_application_class(self):
        return xtensions.TemplateApplication

    
class RedirectRoute(Route):
    url = NullCharField(max_length=255, null=False, blank=False, verbose_name=_("URL"))
    permanent = models.BooleanField(default=False, verbose_name=_("Permanent"))

    class Meta:
        verbose_name = _("Redirect")
        verbose_name_plural = _("Redirects")
        db_table = "xadrpy_router_redirect"

    def get_application_class(self):
        return xtensions.RedirectApplication
