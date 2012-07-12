from django.db import models
from django.utils.translation import ugettext_lazy as _
from xadrpy.models.fields.nullchar_field import NullCharField
import conf
import datetime
from xadrpy.router.models import Route
from xadrpy.models.fields.dict_field import DictField
from django.conf.urls import url
from django.conf import settings
from xadrpy.models.fields.json_field import JSONField
from xadrpy.models.inheritable import TreeInheritable, Inheritable
from xadrpy.auth.models import OwnedModel
from ckeditor.fields import RichTextField
import logging
logger = logging.getLogger("Pages")


class Root(Route):
    name = NullCharField(max_length=255, unique=True, verbose_name=_("Name"))
    layout = models.ForeignKey('Layout', blank=True, null=True, verbose_name=_("Default layout"), related_name="+")
    extra_classes = models.CharField(max_length=255, blank=True, verbose_name = _("Extra classes"), default="")
    resolve = models.CharField(max_length=128, choices=conf.RESOLVES, default=conf.RESOLVE_NORMAL, verbose_name=_("Resolver"))
    
    class Meta:
        verbose_name = _("Pages root")
        verbose_name_plural = _("Pages roots")
        db_table = "xadrpy_pages_root"

    def __unicode__(self):
        return self.name

    def get_urls(self, kwargs={}):
        kwargs.update({'route': self})
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [
            url(self.get_translated_regex(slash=slash), 'xadrpy.contrib.pages.views.root', kwargs=kwargs, name=self.name),
            url(self.get_translated_regex(postfix=self.resolve+slash+"$"), 'xadrpy.contrib.pages.views.root', kwargs=kwargs, name=self.name)
        ]

class Plugin(Inheritable):
    key = models.CharField(max_length=255, unique=True, verbose_name=_("Key"))
    name = NullCharField(max_length=255, verbose_name=_("Name"))
#    templtate = NullCharField(max_length=255, verbose_name=_("Template"))

    class Meta:
        verbose_name = _("Plugin")
        verbose_name_plural = _("Plugins")
        db_table = "xadrpy_pages_plugin"
    
    def __unicode__(self):
        return self.key

class BasePluginItem(models.Model):
    place = models.CharField(max_length=128, verbose_name=_("Place"))
    plugin = models.ForeignKey(Plugin, verbose_name=_("Plugin"), related_name="+")
    weight = models.IntegerField(default=1, verbose_name=_("Weight"))
    disabled = models.BooleanField(default=False, verbose_name=_("Disabled"))

    class Meta:
        abstract = True

class Layout(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    template = models.CharField(max_length=255, blank=True, null=True, choices=conf.TEMPLATES, verbose_name = _("Template"))
    config = DictField()
    plugins = models.ManyToManyField(Plugin, through='LayoutPluginItem', verbose_name=_("Plugins"))

    class Meta:
        verbose_name = _("Layout plugin item")
        verbose_name_plural = _("Layout plugin items")
        db_table = "xadrpy_pages_layout"
    
    def __unicode__(self):
        return self.name

class LayoutPluginItem(BasePluginItem):
    layout = models.ForeignKey(Layout, verbose_name=_("Layout"), related_name="+")

    class Meta:
        verbose_name = _("Layout plugin item")
        verbose_name_plural = _("Layout plugin items")
        db_table = "xadrpy_pages_layout_plugin_item"
    
class BasePage(TreeInheritable, OwnedModel):
    root = models.ForeignKey(Root, verbose_name=_("Root"), related_name="pages")
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"), db_index=True, blank=True, default="")
    head = JSONField(default={})
    view_count = models.IntegerField(default=0, verbose_name = _("View count"))
    extra_classes = models.CharField(max_length=255, blank=True, verbose_name = _("Extra classes"), default="")
    layout = models.ForeignKey(Layout, null=True, blank=True, verbose_name=_("Layout"), related_name="+")
    layout_config = DictField()
    plugins = models.ManyToManyField(Plugin, through='PagePluginItem')
    
    publication_start = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    publication_end = models.DateTimeField(verbose_name = _("Publication end"), null=True, blank=True, db_index=True)

    enable_comments = models.BooleanField(default=True, verbose_name = _("Enable comments"), db_index=True)
    
    class Meta:
        verbose_name = _("Base page")
        verbose_name_plural = _("Base pages")
        db_table = "xadrpy_pages_base_page"

    def __unicode__(self):
        return self.title

class PagePluginItem(BasePluginItem):
    page = models.ForeignKey(BasePage, related_name="+")

    class Meta:
        verbose_name = _("Page plugin item")
        verbose_name_plural = _("Page plugin items")
        db_table = "xadrpy_pages_page_plugin_item"

class Post(BasePage):
    is_featured = models.BooleanField(default=False, verbose_name = _("Is featured"))
    weight = models.IntegerField(default=1, verbose_name=_("Weight"))
    posts = models.ManyToManyField('self', blank=True, null=True, verbose_name = _("Related posts"), db_table="xadrpy_pages_post_posts")
    source = models.URLField(verbose_name=_("Source URL"), blank=True, null=True)
    source_title = NullCharField(max_length=255, verbose_name=_("Source title"), blank=True, null=True)
    excerpt = RichTextField(blank=True, null=True, verbose_name = _("Excerpt"))
    excerpt_image = models.ImageField(upload_to="excerpts", blank=True, null=True, verbose_name = _("Image"))
    lead = RichTextField(blank=True, null=True, verbose_name = _("Lead"))
    lead_image = models.ImageField(upload_to="leads", blank=True, null=True, verbose_name = _("Image"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        db_table = "xadrpy_pages_post"

class Gallery(Post):
    main_image = models.ImageField(upload_to="Gallery", blank=True, null=True, verbose_name = _("Image"))

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galeries")
        db_table = "xadrpy_pages_gallery"

class GalleryImage(models.Model):
    image = models.ImageField(upload_to="Gallery", blank=True, null=True, verbose_name = _("Image"))
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    description = RichTextField(blank=True, null=True, verbose_name = _("Description"))

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galeries")
        db_table = "xadrpy_pages_gallery_image"

    def __unicode__(self):
        return self.title
        

class Menu(Plugin):
    title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"))

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
        db_table = "xadrpy_pages_menu"

    def __unicode__(self):
        return self.title

class Page(BasePage):
    menus = models.ManyToManyField(Menu, verbose_name=_("Menu"),  through='MenuItem')
    menu_title = models.CharField(max_length=255, blank=True, null=True, verbose_name = _("Menu title"))
    menu_image = models.ImageField(upload_to="menuitems", blank=True, null=True, verbose_name = _("Image"))
    menu_depth = models.PositiveIntegerField(default=0, verbose_name=_("Menu depth"))
    posts = models.ManyToManyField(Post, blank=True, null=True, verbose_name = _("Related posts"), db_table="xadrpy_pages_page_posts")
    excerpt = RichTextField(blank=True, null=True, verbose_name = _("Excerpt"))
    excerpt_image = models.ImageField(upload_to="menuitems", blank=True, null=True, verbose_name = _("Image"))
    lead = RichTextField(blank=True, null=True, verbose_name = _("Lead"))
    lead_image = models.ImageField(upload_to="menuitems", blank=True, null=True, verbose_name = _("Image"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    redirect_to = NullCharField(max_length=255, verbose_name=_("Redirect"))
    redirect_permanent = models.BooleanField(default=True, verbose_name=_("Permanent redirect"))
    redirect_target = models.CharField(max_length=32, choices=conf.REDIRECT_TARGETS, blank=True, default=conf.REDIRECT_TARGET_SAME, verbose_name=_("Redirect target"))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        db_table = "xadrpy_pages_page"

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, verbose_name=_("Menu"), related_name="+")
    page = models.ForeignKey(Page, verbose_name=_("Page"), related_name="+")
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="menuitems", blank=True, null=True, verbose_name = _("Image"))
    depth = models.PositiveIntegerField(default=0, verbose_name=_("Depth"))

    class Meta:
        verbose_name = _("Menu item")
        verbose_name_plural = _("Menu items")
        db_table = "xadrpy_pages_menu_item"

    def __unicode__(self):
        return self.title

class Snippet(Plugin):
    content = models.TextField(blank=True, verbose_name=_("Content"))

    class Meta:
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")
        db_table = "xadrpy_pages_snippet"
