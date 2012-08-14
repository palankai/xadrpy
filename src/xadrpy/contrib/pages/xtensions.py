from xadrpy.core.router.base import Application
from django.conf import settings
from django.conf.urls import url
import conf
from django.db.models import permalink
from xadrpy.contrib.plugins.base import Plugin
from xadrpy.contrib.pages.models import SnippetPlace
from django.utils.safestring import mark_safe
from django.core.urlresolvers import resolve
from xadrpy.core.router.models import Route

class PageApplication(Application):

    @permalink
    def get_absolute_url(self):
        return (conf.DEFAULT_VIEW, (),{'route_id': self.route.id})

    def get_urls(self, kwargs={}):
        slash = ""
        if settings.APPEND_SLASH:
            slash = "/"
        return [url(self.get_translated_regex(slash=slash), conf.DEFAULT_VIEW, kwargs=kwargs, name=self.route.name)]

class SnippetPlugin(Plugin):
    alias = "x-snippet"
    model = SnippetPlace
        
    def render(self, context):
        if self.place:
            return mark_safe(self.place.body)
        return self.render_template()

class HMenuPlugin(Plugin):
    alias = "x-hmenu"
    template="xadrpy/pages/plugins/hmenu.html"

    def render(self, context):
        parent = None
        request = context.get('request')
        func, args, kwargs = resolve(request.path)
        selected=None
        if hasattr(request,'route'):
            selected = request.route
        if 'route' in context:
            selected = context['route']
        #selected = kwargs.get('route', context.get('route', hasattr(request,'route') and request.route.id))
        if not selected:
            selected_key = context.get('route_key', getattr(request, 'route_key', None))
            if selected_key:
                selected = Route.objects.get(key=selected_key)
        ancestors=[]
        if selected:
            ancestors = [ancestor.id for ancestor in selected.get_ancestors(include_self=False)]
        context.update({
            'items': Route.objects.filter(parent=parent, visible=True, enabled=True),
            'selected': selected,
            'ancestors': ancestors,
            'parent': parent,
        })
        return self.render_template(context)
