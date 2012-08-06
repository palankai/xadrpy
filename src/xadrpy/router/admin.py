from django.contrib.admin import site, ModelAdmin
from models import Route
from forms import RouteAdminForm
from django.utils.translation import ugettext_lazy as _
from xadrpy.router.models import IncludeRoute

class RouteAdmin(ModelAdmin):
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