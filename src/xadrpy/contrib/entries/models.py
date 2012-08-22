from xadrpy.core.models.fields.nullchar_field import NullCharField
from django.db import models
import conf 
from xadrpy.core.access.models import OwnedModel
from xadrpy.contrib.pages.models import Page
import datetime
from xadrpy.core.models.inheritable import TreeInheritable
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from xadrpy.core.i18n.models import Translation
from xadrpy.core.i18n.fields import TranslationForeignKey
from xadrpy.core.models.fields.language_code_field import LanguageCodeField
from django.dispatch.dispatcher import receiver
from xadrpy.core.router.signals import prepend_route_urls
from django.db.models import permalink
from managers import EntryManager, CategoryManager
from xadrpy.core.preferences.libs import prefs
from xadrpy.contrib.entries.xtensions import MonthBasedEntriesApplication

class Column(Page):
    post_comments_enabled = models.BooleanField(default=True, verbose_name = _("Comments enabled"), db_index=True)
    post_comments_unlocked = models.BooleanField(default=True, verbose_name = _("Comments unlocked"), db_index=True)
    
    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        db_table = "xadrpy_entries_column"

    def __unicode__(self):
        return self.title

    def get_application_class(self):
        return MonthBasedEntriesApplication
    
    def get_entries(self, **kwargs):
        return Entry.objects.get_entries_for_column(self, **kwargs)
    
    def get_entry(self, **kwargs):
        return self.get_entries(**kwargs).get()
    
    def to_dict(self):
        return self.__dict__


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("Parent"))    
    column = models.ForeignKey(Column, blank=True, null=True, related_name="categories", verbose_name=_("Column"))
    language_code = LanguageCodeField(blank=True, null=True, default=None, verbose_name=_("Language code"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"))
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))
    
    tree = TreeManager()
    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "xadrpy_entries_category"
    
    def __unicode__(self):
        return self.title
    
    def get_title(self):
        return self.translation().title
    
    def get_entry_count(self, **kwargs):
        return self.get_entries(**kwargs).count()

    def get_entries(self, **kwargs):
        return Entry.objects.get_entries_for_category(self, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return ("x-entries-categories", (), {'slug': self.translation().slug})
    
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
        return self.language_code+": "+unicode(self.origin)
    

    class Meta:
        verbose_name = _("Category translation")
        verbose_name_plural = _("Category translations")
        db_table = "xadrpy_entries_category_translation"

CategoryTranslation.register(Category)
    
    
class Entry(TreeInheritable, OwnedModel):
    column = models.ForeignKey(Column, verbose_name=_("Column"), related_name="+")
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    language_code = LanguageCodeField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, verbose_name=_("URL part"), db_index=True)
    view_count = models.IntegerField(default=0, verbose_name = _("View count"))
    categories = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_("Categories"), db_table="xadrpy_blog_entry_categories", related_name="entries")
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name = _("Publication start"), db_index=True)
    published = models.BooleanField(default=False, verbose_name=_("Is published"))

    comments_enabled = models.BooleanField(default=True, verbose_name = _("Comments enabled"), db_index=True)
    comments_unlocked = models.BooleanField(default=True, verbose_name = _("Comments unlocked"), db_index=True)

    featured = models.BooleanField(default=False, verbose_name = _("Is featured"))
    weight = models.IntegerField(default=1, verbose_name=_("Weight"))

    entries = models.ManyToManyField('self', blank=True, null=True, verbose_name = _("Related entries"), db_table="xadrpy_blog_entry_entries")
    pages = models.ManyToManyField(Page, blank=True, null=True, verbose_name=_("Related pages"), db_table="xadrpy_blog_entry_pages")

    source = NullCharField(max_length=255, verbose_name=_("Source title"), blank=True, null=True)
    source_url = models.URLField(verbose_name=_("Source URL"), blank=True, null=True)

    image = models.ImageField(upload_to="entries", blank=True, null=True, verbose_name = _("Image"))
    content = RichTextField(blank=True, null=True, verbose_name = _("Content"))

    meta_title = models.CharField(max_length=255, blank=True, verbose_name=_("Meta title"), default="")
    overwrite_meta_title = models.BooleanField(default=False, verbose_name=_("Overwrite meta title"))
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name=_("Meta keywords"), default="")
    meta_description = models.TextField(blank=True, verbose_name=_("Meta description"), default="")

    objects = EntryManager()

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        db_table = "xadrpy_entries_entries"

    def __unicode__(self):
        return self.title

    def can_render(self):
        if not self.column.can_render() or not self.published:
            return False
        if datetime.datetime.now().replace(tzinfo=None) < self.pub_date.replace(tzinfo=None):
            return False
        return True    
    
    def get_content_pages(self):
        return conf.PAGE_BREAK_RE.split(self.content)

    def get_content(self):
        return "".join(self.get_content_pages())

    def get_content_tail(self):
        tail = self.get_content_pages()[1:]
        if not len(tail): return ""
        return "".join(tail)

    def get_content_head(self):
        return self.get_content_pages()[0]
    
    def get_excerpt(self):
        return self.get_content_head()
    
    def get_simple_excerpt(self):
        return strip_tags(self.get_excerpt())
    
    def get_title(self):
        return self.title
    
    def get_pub_date(self):
        return self.pub_date.date()
    
    def get_absolute_url(self):
        return self.get_column().app.get_entry_absolute_url(self)
    
    def is_comments_enabled(self):
        return self.get_column().post_comments_enabled and self.comments_enabled and prefs("entry_comments_enabled", namespace="x-blog", default=True)

    def get_meta_title(self):
        if self.overwrite_meta_title and self.meta_title:
            return self.meta_title
        self_title = self.meta_title or self.title 
        if self.get_parent() and self.get_parent().get_meta_title():
            self_title = self_title + " | " + self.get_parent().get_meta_title() + " | " + self.column.get_meta().get_meta_title()
        else:
            self_title = self_title + " | " + self.column.get_meta().get_meta_title()
        return self_title

    def get_meta_keywords(self):
        if self.meta_keywords:
            return self.meta_keywords
        return self.get_column().get_meta().get_meta_keywords()

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.get_simple_excerpt().strip()
    
    def get_column(self):
        return self.column.descendant
    
    def increment_view_count(self, request):
        if request.user.is_staff or self.user == request.user: return
        self.view_count = models.F("view_count")+1
        self.save() 

class Image(models.Model):
    entry = models.ForeignKey(Entry, related_name="images")
    position = models.IntegerField(default=1, verbose_name=_("Position"))
    image = models.ImageField(upload_to="entries", blank=True, null=True, verbose_name = _("Image"))
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255)
    description = RichTextField(blank=True, null=True, verbose_name = _("Description"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        db_table = "xadrpy_entries_image"
        ordering = ['position']

    def __unicode__(self):
        return self.title

@receiver(prepend_route_urls)
def prepend_blog_urls(sender, urlpatterns, **kwargs):
    from django.conf.urls import patterns, url
    urlpatterns+=patterns("",
        url(_('^categories/$'), 'xadrpy.contrib.entries.views.categories', name="x-entries-categories"),
        url(_('^categories/(?P<slug>.+)/$'), 'xadrpy.contrib.entries.views.categories', name="x-entries-categories")
    )
