from django.contrib.admin import site, ModelAdmin
from models import Page
from django.utils.translation import ugettext_lazy as _ 
from xadrpy.contrib.pages.forms import PageAdminForm, PageCreateAdminForm
from django.contrib.admin.options import StackedInline
from xadrpy.contrib.pages.models import PageTranslation
from django.conf.urls import patterns
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from xadrpy.core.router.admin import BaseRouteAdmin

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

class PageAdmin(BaseRouteAdmin):
    form = PageAdminForm
    add_form = PageCreateAdminForm
    fieldsets = (
        (None, {
            'fields': ('parent','title','slug', 'content','application_name')
        }),
        (_("SEO"), {
            'fields': ('overwrite_meta_title', 'meta_title', 'meta_description', 'meta_keywords')
        }),
        (_('Publication'), {
            'fields': ('user', 'group', 'pub_date', 'published', 'enabled', 'visible', 'show_content', 'comments_enabled', 'comments_unlocked', 'i18n')
        }),
        (_('Design'), {
            'fields': ('menu_title', 'layout_name', 'skin_name', 'extra_classes', 'site', 'master', 'language_code', 'image', 'name',)
        }),
        (_('Extra'), {
            'fields': ('created','modified', 'view_count', )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('parent','title','slug', 'content',)
        }),
    )
    list_display = ('depth_title','slug', 'language_code', 'pub_date','enabled','published','visible','view_count')
    list_display_links = ('depth_title', 'slug')
    list_filter = ('user', 'group', 'enabled','published','visible','show_content','comments_enabled','i18n','site','master','language_code')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title','slug','name')
    readonly_fields = ('created', 'modified',)
    inlines = (PageTranslationInlineAdmin,)

#    def get_formsets(self, request, obj=None):
#        if not obj:
#            for inline in []:
#                yield inline.get_formset(request, obj)
#        else:
#            for inline in self.get_inline_instances(request):
#                yield inline.get_formset(request, obj)
#
#    def get_fieldsets(self, request, obj=None):
#        if not obj:
#            return self.add_fieldsets
#        return super(PageAdmin, self).get_fieldsets(request, obj)
#    
#    def get_form(self, request, obj=None, **kwargs):
#        """
#        Use special form during user creation
#        """
#        defaults = {}
#        if obj is None:
#            defaults.update({
#                'form': self.add_form,
#                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
#            })
#        defaults.update(kwargs)
#        return super(PageAdmin, self).get_form(request, obj, **defaults)    
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        for k in form._meta_fields:
            if form.cleaned_data[k]:
                obj.prefs.reset(k, form.cleaned_data[k] or None)
            else:
                obj.prefs.reset(k, None)
        obj.save()    
    
    def menu_title(self, obj):
        return obj.prefs.get("menu_title")

    def meta_title(self, obj):
        return obj.prefs.get("meta_title")
   
    def depth_title(self, obj):
        depth = "".join([" ----- " for i in range(obj.level)])
        return depth + obj.title
    
    def list_actions(self, obj):
        acts = []
        if obj.get_previous_sibling():
            acts.append("""<a href="%s">%s</a>""" % ('move_up/%s/' % obj.id ,unicode(_("Move up"))))
        else:
            acts.append("""<span>%s</span>""" % unicode(_("Move up")))
        if obj.get_next_sibling():
            acts.append("""<a href="%s">%s</a>""" % ('move_down/%s/'% obj.id ,unicode(_("Move down"))))
        else:
            acts.append("""<span>%s</span>""" % unicode(_("Move down")))
        return " | ".join(acts)
    list_actions.allow_tags = True
    list_actions.short_description = _("Actions")

#    def get_urls(self):
#        urls = super(PageAdmin, self).get_urls()
#        my_urls = patterns('',
#            (r'^move_up/(?P<pk>[0-9]+)/$',  self.move_up),
#            (r'^move_down/(?P<pk>[0-9]+)/$',  self.move_down)
#        )
#        return my_urls + urls
#
#    def move_up(self, request, pk):
#        obj = self.model.objects.get(pk=pk)
#        obj.move_to(obj.get_previous_sibling(), "left")
#        return HttpResponseRedirect(reverse('admin:pages_page_changelist'))
#
#    def move_down(self, request, pk):
#        obj = self.model.objects.get(pk=pk)
#        obj.move_to(obj.get_next_sibling(), "right")
#        return HttpResponseRedirect(reverse('admin:pages_page_changelist'))

site.register(Page, PageAdmin)
