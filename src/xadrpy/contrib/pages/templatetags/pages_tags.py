from django.template.loader import render_to_string
from xadrpy.router.models import Route
from django.core.urlresolvers import resolve
from xadrpy.templates.lib import WidgetLibrary, XWidgetBase
from django.utils import importlib
from xadrpy.contrib.pages.models import PluginStore
from xadrpy.contrib.pages.libs import PLUGIN_CACHE
 
register = WidgetLibrary()

@register.simple_tag(takes_context=True)
def menu(context, parent=None, template="xadrpy/pages/menu.html", selected=None, ancestors=[]):
    request = context.get('request')
    if parent == None:
        func, args, kwargs = resolve(request.path)
        selected = kwargs.get('route', context.get('route', getattr(request,'route', None)))
        if not selected:
            selected_key = context.get('route_key', getattr(request, 'route_key', None))
            if selected_key:
                selected = Route.objects.get(key=selected_key)
        if selected:
            ancestors = [ancestor.id for ancestor in selected.get_ancestors(include_self=False)]
    ctx = {
        'items': Route.objects.filter(parent=parent, menu_title__isnull=False),
        'selected': selected,
        'ancestors': ancestors,
        'parent': parent,
    }
    return render_to_string(template, ctx, context)


class PluginNode(XWidgetBase):

    def value(self, context, name, placeholder, *args, **kwargs):
        if name in PLUGIN_CACHE:
            plugin = PLUGIN_CACHE[name]
        else:
            module_name, widget_name = name.rsplit(".",1)
            module = importlib.import_module(module_name)
            plugin = getattr(module, widget_name)
        try:
            plugin_instance = plugin(placeholder)
            plugin_instance.init_template(kwargs.pop('TEMPLATE', None))
            return plugin_instance.render(context, *args, **kwargs)
        except Exception, e:
            return "Exception: %s" % e

register.widget('plugin')(PluginNode)
