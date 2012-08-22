from xadrpy.core.templates.base import WidgetLibrary
from xadrpy.contrib.toolbar import conf
from django.template.loader import render_to_string
from xadrpy.contrib.toolbar.base import Toolbar
from django.template.base import Context
import logging
logger = logging.getLogger("xadrpy.contrib.toolbar.templatetags.toolbar")
register = WidgetLibrary()


@register.simple_tag(takes_context=True)
def toolbar_styles(context):
    request = context['request']
    if request.user.is_anonymous(): return ""
    out = [
        '<link rel="stylesheet" type="text/css" href="' + conf.STATIC_URL + 'xadrpy/toolbar/toolbar.css" media="screen" />'
    ]
    return "\n".join(out)


@register.simple_tag(takes_context=True)
def toolbar_scripts(context, cls="x-toolbar"):
    request = context['request']
    if request.user.is_anonymous(): return ""
    out = [
        '<script type="text/javascript" src="' + conf.STATIC_URL + 'xadrpy/toolbar/toolbar.js"></script>'
    ]
    return "\n".join(out)

@register.simple_tag(takes_context=True)
def toolbar(context):
    request = context['request']
    if request.user.is_anonymous(): return ""
    toolbar = Toolbar(request)
    if hasattr(request, "route") and request.route:
        request.route.app.toolbar_setup(context, toolbar)
    if hasattr(request, "xtensions"):
        for xtension in [xt for xt in request.xtensions if hasattr(xt, "toolbar_setup")]:
            xtension.toolbar_setup(context, toolbar)
    ctx = {
        'toolbar': toolbar
    }
    return render_to_string("xadrpy/toolbar/toolbar.html", ctx, context)

@register.simple_tag(takes_context=True)
def render_toolbar_item(context, toolbar_item):
    return toolbar_item.render(context)
