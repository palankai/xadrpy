from xadrpy.core.templates.base import WidgetLibrary
from xadrpy.core.theming.libs import get_current_theme
register = WidgetLibrary()
from xadrpy.core.theming import conf

@register.simple_tag(takes_context=True)
def skin_styles(context):
    request = context['request']
    skin_name = request.theming_skin
    if not skin_name: return ""
    theme = get_current_theme()
    style_buffer = []
    for style in theme.get_skin_styles(skin_name):
        if 'media' in style:
            tag = conf._MEDIA_STYLE_TAG % style
        else:
            tag = conf._SIMPLE_STYLE_TAG % style
        if 'condition' in style:
            tag = conf._CONDITION % (style['condition'], tag)
        style_buffer.append(tag)
    return "\n".join(style_buffer)

@register.simple_tag(takes_context=True)
def skin_scripts(context):
    request = context['request']
    skin_name = request.theming_skin
    if not skin_name: return ""
    theme = get_current_theme()
    out = []
    for filename in theme.get_skin_scripts(skin_name):
        out.append(conf._SCRIPT_TAG % filename)
    return "\n".join(out)
