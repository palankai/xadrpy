from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from xadrpy.models.fields.nullchar_field import NullCharField
import conf
import datetime



class Channel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))

class Page(models.Model):
    language_code = NullCharField(max_length=5, blank=True, null=True)

    parent = models.ForeignKey('self', blank=True, null=True, verbose_name = _("Parent"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("META title"))
    meta_description = models.TextField(blank=True, null=True, verbose_name = _("META description"))
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("META keywords"))
    meta_robots = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("META robots"), default="INDEX, FOLLOW")
    meta_canonical = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("META canonical"))
    menu_title = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("Menu title"))

    view_count = models.IntegerField(default=0, verbose_name = _("View count"))
    extra_classes = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("Extra classes"))
    template = models.CharField(max_length=255, blank=True, null=True, choices=conf.TEMPLATES, verbose_name = _("Template"))

    publication = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication"))
    visibility = models.CharField(max_length=3, choices=conf.VISIBILITIES, default=conf.DEFAULT_VISIBILITY, verbose_name = _("Visibility"))
    state = models.CharField(choices=conf.ENTRY_STATES, default=conf.DEFAULT_STATE, max_length=3, verbose_name = _("Status"))
    enable_comments = models.BooleanField(default=True, verbose_name = _("Enable comments"))
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("Password"))
    is_featured = models.BooleanField(default=False, verbose_name = _("Is featured"))
    weight = models.IntegerField(default=1)

    related = models.ManyToManyField('self', blank=True, null=True, verbose_name = _("Related posts"))
    
    source = models.URLField(verbose_name=_("Source"), blank=True, null=True)
    source_title = models.URLField(verbose_name=_("Source title"), blank=True, null=True)
    
    image = models.ImageField(upload_to="posts", blank=True, null=True, verbose_name = _("Image"))

    excerpt = HTMLField(blank=True, null=True, verbose_name = _("Excerpt"))
    content = HTMLField(blank=True, null=True, verbose_name = _("Content"))

    entries = models.ManyToManyField(PostBase, blank=True, null=True, verbose_name = _("Posts"))
    
