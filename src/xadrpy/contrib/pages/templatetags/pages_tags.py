from django.template.loader import render_to_string
from xadrpy.core.router.models import Route
from django.core.urlresolvers import resolve
from xadrpy.core.templates.base import WidgetLibrary
 
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
        'items': Route.objects.filter(parent=parent, visible=True, enabled=True),
        'selected': selected,
        'ancestors': ancestors,
        'parent': parent,
    }
    return render_to_string(template, ctx, context)



