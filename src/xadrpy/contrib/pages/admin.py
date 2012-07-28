from django.contrib.admin import site, ModelAdmin
from models import Page
from django.utils.translation import ugettext_lazy as _ 
from xadrpy.contrib.pages.forms import PageAdminForm
from django.contrib.admin.options import StackedInline
from xadrpy.contrib.pages.models import PageTranslation

class PageTranslationInlineAdmin(StackedInline):
    model = PageTranslation
    fieldsets = (
        (None, {
            'fields': ('language_code','title','slug', 'image','content')
        }),
        (_("SEO"), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )

class PageAdmin(ModelAdmin):
    form = PageAdminForm
    fieldsets = (
        (None, {
            'fields': ('title','slug', 'content',)
        }),
        (_("SEO"), {
            'fields': ('overwrite_meta_title', 'meta_title', 'meta_description', 'meta_keywords')
        }),
        (_('Publication'), {
            'fields': ('user', 'group', 'pub_date', 'published', 'enabled', 'visible', 'show_content', 'comments_enabled', 'comments_unlocked', 'i18n')
        }),
        (_('Design'), {
            'fields': ('menu_title', 'layout_name', 'skin_name', 'extra_classes', 'view_name','site', 'master', 'language_code', 'image', 'name',)
        }),
        (_('Extra'), {
            'fields': ('created','modified', 'view_count', )
        }),
    )
    list_display = ('title','slug', 'meta_title','menu_title','language_code', 'pub_date','created','modified', 'name', 'user', 'group', 'enabled','published','visible','show_content','comments_enabled','comments_unlocked','view_count')
    list_display_links = ('title', 'slug')
    list_filter = ('user', 'group', 'enabled','published','visible','show_content','comments_enabled','i18n','site','master','language_code')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title','slug','meta_title','name')
    readonly_fields = ('created', 'modified',)
    inlines = (PageTranslationInlineAdmin,)
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        for k in form._meta_fields:
            obj.meta[k] = form.cleaned_data[k] 
        obj.save()    
    
    def menu_title(self, obj):
        return obj.get_meta().meta['menu_title']

site.register(Page, PageAdmin)
