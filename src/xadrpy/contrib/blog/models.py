from xadrpy.models.fields.nullchar_field import NullCharField
from django.db import models
import conf 
from xadrpy.access.models import OwnedModel, prefs
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
from django.utils.html import strip_tags
from xadrpy.i18n.models import Translation
from xadrpy.i18n.fields import TranslationForeignKey
from xadrpy.models.fields.language_code_field import LanguageCodeField

class Column(Page):
    post_comments_enabled = models.BooleanField(default=True, verbose_name = _("Comments enabled"), db_index=True)
    post_comments_unlocked = models.BooleanField(default=True, verbose_name = _("Comments unlocked"), db_index=True)

    resolver = models.CharField(max_length=255, choices=conf.RESOLVERS, default=conf.DEFAULT_RESOLVER, verbose_name=_("Resolver"))
    
    default_view = "xadrpy.contrib.blog.views.column"
    
    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        db_table = "xadrpy_blog_column"

    def __unicode__(self):
        return self.title

    def get_template(self):
        return "xadrpy/blog/column.html"
    
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
    language_code = LanguageCodeField(blank=True, null=True, default=None, verbose_name=_("Language code"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"))
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))
    
    tree = TreeManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "xadrpy_blog_category"
    
    def __unicode__(self):
        return self.title
    
class CategoryTranslation(Translation):
    origin = TranslationForeignKey(Category, related_name="+")
    language_code = LanguageCodeField()

    title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"), default="")
    slug = models.SlugField(max_length=255, blank=True, verbose_name=_("URL part"), default="")
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))
    
    def set_defaults(self, origin):
        self.title = origin.title
        self.slug = origin.slug
        self.description = origin.description
    
    def __unicode__(self):
        return (self.language_code or "")+": "+unicode(self.origin)

    class Meta:
        verbose_name = _("Category translation")
        verbose_name_plural = _("Category translations")
        db_table = "xadrpy_blog_category_translation"

CategoryTranslation.register(Category)
    
    
class Post(TreeInheritable, OwnedModel):
    column = models.ForeignKey(Column, verbose_name=_("Column"), related_name="posts")
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    language_code = LanguageCodeField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"), db_index=True)
    view_count = models.IntegerField(default=0, verbose_name = _("View count"))
    categories = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_("Categories"), db_table="xadrpy_blog_post_categories")
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    published = models.BooleanField(default=False, verbose_name=_("Is published"))

    comments_enabled = models.BooleanField(default=True, verbose_name = _("Comments enabled"), db_index=True)
    comments_unlocked = models.BooleanField(default=True, verbose_name = _("Comments unlocked"), db_index=True)

    featured = models.BooleanField(default=False, verbose_name = _("Is featured"))
    weight = models.IntegerField(default=1, verbose_name=_("Weight"))

    posts = models.ManyToManyField('self', blank=True, null=True, verbose_name = _("Related posts"), db_table="xadrpy_blog_post_posts")
    pages = models.ManyToManyField(Page, blank=True, null=True, verbose_name=_("Related pages"), db_table="xadrpy_blog_post_pages")

    source = NullCharField(max_length=255, verbose_name=_("Source title"), blank=True, null=True)
    source_url = models.URLField(verbose_name=_("Source URL"), blank=True, null=True)

    image = models.ImageField(upload_to="posts", blank=True, null=True, verbose_name = _("Image"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    meta_title = models.CharField(max_length=255, blank=True, verbose_name=_("Meta title"), default="")
    overwrite_meta_title = models.BooleanField(default=False, verbose_name=_("Overwrite meta title"))
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name=_("Meta keywords"), default="")
    meta_description = models.TextField(blank=True, verbose_name=_("Meta description"), default="")

    objects = TreeInheritableManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        db_table = "xadrpy_blog_post"
    
    def get_template(self):
        return conf.DEFAULT_TEMPLATE

    def can_render(self):
        if not self.column.can_render() or not self.published:
            return False
        if datetime.datetime.now().replace(tzinfo=None) < self.pub_date.replace(tzinfo=None):
            return False
        return True    
    
    def render_to_response(self, request, context={}):
        template = self.get_template()
        
        context.update({
            'page': self.column,
            'post': self,
        })
        return render_to_response(template, context, RequestContext(request))
    
    def get_content_pages(self):
        return conf.PAGE_BREAK_RE.split(self.content)

    def get_content(self):
        return "".join(self.get_content_pages())

    def get_content_tail(self):
        return "".join(self.get_content_pages())[1:]

    def get_content_head(self):
        return "".join(self.get_content_pages())[0]
    
    def get_excerpt(self):
        return self.get_content_head()
    
    def get_simple_excerpt(self):
        return strip_tags(self.get_excerpt())
    
    def get_absolute_url(self):
        return self.get_column().get_resolver().get_absolute_url(self)
    
    def is_comments_enabled(self):
        return self.get_column().post_comments_enabled and self.comments_enabled and prefs("comments_enabled", namespace="x-blog")

    def get_meta_title(self):
        if self.overwrite_meta_title and self.meta_title:
            return self.meta_title
        self_title = self.meta_title or self.title 
        if self.get_parent() and self.get_parent().get_meta_title():
            self_title = self_title + " | " + self.get_parent().get_meta_title()
        return self_title

    def get_meta_keywords(self):
        if self.meta_keywords:
            return self.meta_keywords
        return self.get_column().get_meta_keywords()

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.get_simple_excerpt()
    
    def get_column(self):
        return self.column.descendant


class Image(models.Model):
    post = models.ForeignKey(Post, related_name="images")
    position = models.IntegerField(default=1, verbose_name=_("Position"))
    image = models.ImageField(upload_to="posts", blank=True, null=True, verbose_name = _("Image"))
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255)
    description = RichTextField(blank=True, null=True, verbose_name = _("Description"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        db_table = "xadrpy_blog_image"
        ordering = ['position']

    def __unicode__(self):
        return self.title
