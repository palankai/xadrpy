from django.contrib.admin import site, ModelAdmin
from models import Route, IncludeRoute
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import logging
from django.forms.widgets import Select
logger = logging.getLogger("xadrpy.router.admin")

class BaseRouteAdmin(ModelAdmin):

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        fields = context['adminform'].form.fields
        model = context['adminform'].form._meta.model
        if "application_name" in fields:
            application_name = fields['application_name']
            applications = model.get_application_choices() or [('',_("Default application"))]
            application_name.widget = Select(None, applications)
        return super(BaseRouteAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        if request.GET.get('from-toolbar') == "1":
            return HttpResponse("<script type='text/javascript'>window.opener.location.reload();window.close();</script>");
        return ModelAdmin.response_change(self, request, obj)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if request.GET.get('from-toolbar') == "1":
            return HttpResponse("<script type='text/javascript'>window.opener.location.reload();window.close();</script>");
        return ModelAdmin.response_add(self, request, obj, post_url_continue)
    
    def get_urls(self):
        urls = super(BaseRouteAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name

        my_urls = patterns('',
            url(r'^move_up/(?P<pk>[0-9]+)/$',  self.move_up, name="x-%s-%s-admin-forward" % info),
            url(r'^move_down/(?P<pk>[0-9]+)/$',  self.move_down, name="x-%s-%s-admin-backward" % info),
            url(r'^delete/(?P<pk>[0-9]+)/$',  self.delete, name="x-%s-%s-admin-delete" % info),
        )
        return my_urls + urls

    def delete(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return HttpResponseRedirect(request.GET.get('next', reverse('admin:router_route_changelist')))

    def move_up(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.move_to(obj.get_previous_sibling(), "left")
        return HttpResponseRedirect(request.GET.get('next', reverse('admin:router_route_changelist')))

    def move_down(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.move_to(obj.get_next_sibling(), "right")
        return HttpResponseRedirect(request.GET.get('next', reverse('admin:router_route_changelist')))
    

class RouteAdmin(BaseRouteAdmin):
    fieldsets = (
        (None, {
            'fields': ('parent','title','slug')
        }),
        (None, {
            'fields': ('application_name',)
        }),
        (_('Publication'), {
            'fields': ('enabled', 'visible', 'i18n')
        }),
        (_('Design'), {
            'fields': ('site', 'master', 'language_code', 'image', 'name', )
        }),
        (_('Extra'), {
            'fields': ('created','modified', )
        }),
    )
    readonly_fields = ('created', 'modified',)
    list_display = ('list_actions','depth_title','slug', 'language_code', 'enabled','visible')
    list_display_links = ('depth_title', 'slug')
    list_filter = ('enabled','visible','i18n','site','master','language_code')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title','slug','name')
    readonly_fields = ('created', 'modified',)

    def list_actions(self, obj):
        obj = Route.objects.get(pk=obj.id)
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

    def menu_title(self, obj):
        return obj.get_meta().meta.get('menu_title',"")

    def meta_title(self, obj):
        return obj.get_meta().meta.get('meta_title',"")
    
    def depth_title(self, obj):
        depth = "".join([" ----- " for i in range(obj.level)])
        return depth + obj.title


class IncludeRouteAdmin(RouteAdmin):
    fieldsets = (
        (None, {
            'fields': ('parent','title','slug')
        }),
        (None, {
            'fields': ('include_name', 'namespace', 'name')
        }),
        (_('Publication'), {
            'fields': ('enabled', 'visible', 'i18n')
        }),
        (_('Design'), {
            'fields': ('site', 'master', 'language_code', 'image', 'application_name')
        }),
        (_('Extra'), {
            'fields': ('created','modified', )
        }),
    )
    

site.register(Route, RouteAdmin)
site.register(IncludeRoute, IncludeRouteAdmin)