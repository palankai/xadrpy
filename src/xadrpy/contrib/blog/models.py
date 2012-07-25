from xadrpy.models.fields.nullchar_field import NullCharField
from django.db import models
import conf 
from xadrpy.auth.models import OwnedModel
from xadrpy.contrib.pages.models import Page
import datetime
from xadrpy.models.inheritable import TreeInheritable, TreeInheritableManager
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import importlib

class Column(Page):
    resolver = models.CharField(max_length=255, choices=conf.RESOLVERS, default=conf.DEFAULT_RESOLVER, verbose_name=_("Resolver"))
    
    list_layout = models.ForeignKey(Page, verbose_name=_("Default list layout"), related_name="+", blank=True, null=True)
    list_extra_classes = models.CharField(max_length=255, blank=True)

    post_layout = models.ForeignKey(Page, verbose_name=_("Default post layout"), related_name="+", blank=True, null=True)
    post_extra_classes = models.CharField(max_length=255, blank=True)
    
    default_view = "xadrpy.contrib.blog.views.column"
    default_template = "xadrpy/blog/column.html"
    
    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        db_table = "xadrpy_blog_column"

    def __unicode__(self):
        return self.title
    
    def get_list_layout(self):
        return self.list_layout

    def get_post_layout(self):
        return self.post_layout
    
    def get_signature(self):
        signature = super(Column, self).get_signature()
        return signature+"-"+self.resolver
    
    def get_resolver(self):
        if hasattr(self, '_resolver'):
            return self._resolver
        module_name, class_name = self.resolver.rsplit('.',1)
        module = importlib.import_module(module_name)
        resolver_class = getattr(module, class_name)
        conf.RESOLVERS_CACHE[self.resolver] = resolver_class
        self._resolver = resolver_class(self)
        return self._resolver

    def get_urls(self, kwargs={}):
        resolver = self.get_resolver()
        return resolver.get_urls(kwargs)

class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("Parent"))    
    column = models.ForeignKey(Column, blank=True, null=True, related_name="categories", verbose_name=_("Column"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"))
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))

    layout = models.ForeignKey(Page, verbose_name=_("Layout"), related_name="+")
    extra_classes = models.CharField(max_length=255, blank=True)
    
    tree = TreeManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "xadrpy_blog_category"
    
    def __unicode__(self):
        return self.title
    
class BasePost(TreeInheritable, OwnedModel):
    column = models.ForeignKey(Column, verbose_name=_("Column"), related_name="posts")
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"), db_index=True)
    view_count = models.IntegerField(default=0, verbose_name = _("View count"))
    layout = models.ForeignKey(Page, null=True, blank=True, verbose_name=_("Layout"), related_name="+")
    extra_classes = models.CharField(max_length=255, blank=True, verbose_name = _("Extra classes"), default="")
    categories = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_("Categories"), db_table="xadrpy_blog_post_categories")
    publication = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    publication_end = models.DateTimeField(verbose_name = _("Publication end"), null=True, blank=True, db_index=True)
    status = models.CharField(max_length=16, choices=conf.POST_STATES, default='DRA')

    enable_comments = models.BooleanField(default=True, verbose_name = _("Enable comments"), db_index=True)
    lock_comments = models.BooleanField(default=False, verbose_name = _("Lock comments"), db_index=True)

    is_featured = models.BooleanField(default=False, verbose_name = _("Is featured"))
    weight = models.IntegerField(default=1, verbose_name=_("Weight"))

    posts = models.ManyToManyField('self', blank=True, null=True, verbose_name = _("Related posts"), db_table="xadrpy_blog_post_posts")
    pages = models.ManyToManyField(Page, blank=True, null=True, verbose_name=_("Related pages"), db_table="xadrpy_blog_post_pages")

    source = NullCharField(max_length=255, verbose_name=_("Source title"), blank=True, null=True)
    source_url = models.URLField(verbose_name=_("Source URL"), blank=True, null=True)

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta title"))
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta keywords"))
    meta_description = models.TextField(blank=True, null=True, verbose_name=_("Meta description"))
    meta_robots = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta robots"))
    meta_cannonical = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Meta cannoncical"))


    objects = TreeInheritableManager()

    class Meta:
        verbose_name = _("Base post")
        verbose_name_plural = _("Base posts")
        db_table = "xadrpy_blog_base_post"
    
    def get_layout(self):
        if self.layout:
            return self.layout
        return self.column.get_post_layout()
    
    def get_template(self):
        layout = self.get_layout()
        if layout:
            return layout.template
        return conf.DEFAULT_TEMPLATE

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
            'page': self.column,
            'post': self,
            'layout': layout
        })
        return render_to_response(template, context, RequestContext(request))
    
    def get_excerpt(self):
        return ""
        
    def get_absolute_url(self):
        return self.column.get_resolver().get_absolute_url(self)

class Post(BasePost):
    excerpt = RichTextField(blank=True, null=True, verbose_name = _("Excerpt"))
    excerpt_image = models.ImageField(upload_to="excerpts", blank=True, null=True, verbose_name = _("Image"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        db_table = "xadrpy_blog_post"

    def get_excerpt(self):
        return self.excerpt or self.content


class Gallery(BasePost):
    image = models.ImageField(upload_to="gallery", blank=True, null=True, verbose_name = _("Image"))
    description = RichTextField(blank=True, null=True, verbose_name = _("Excerpt"))

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galeries")
        db_table = "xadrpy_blog_gallery"

class GalleryImage(models.Model):
    image = models.ImageField(upload_to="Gallery", blank=True, null=True, verbose_name = _("Image"))
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255)
    description = RichTextField(blank=True, null=True, verbose_name = _("Description"))

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galeries")
        db_table = "xadrpy_blog_gallery_image"

    def __unicode__(self):
        return self.title
