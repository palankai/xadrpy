from xadrpy.core.templates.base import WidgetLibrary, XWidgetBase
from django.template.loader import render_to_string
register = WidgetLibrary()

class StylesNode(XWidgetBase):

    def value(self, context, *args, **kwargs):
        request = context.get('request')
        route = getattr(request, 'route', None)
        theme = getattr(request, "theme", None)
        TEMPLATE = kwargs.pop("TEMPLATE", None)
        if not theme and not TEMPLATE:
            return ""
        if not theme:
            return TEMPLATE.render(context)
        
        styles = []
        for library in theme.get_libraries():
            for style in library.get_styles():
                styles.append({"href": style, "type": "text/css", "rel":"stylesheet" })
        for style in theme.get_styles():
            styles.append({"href": style, "type": "text/css", "rel":"stylesheet" })

        skin_name = route and route.get_meta().get_skin_name() or None
        skin = skin_name and theme.get_skins()[skin_name] or theme.get_default_skin() or {'source':[]}
        for style_name in skin['source']:
            style = theme.style(style_name)
            for style_file in style['files']:
                styles.append({"href": style_file, "type": "text/css", "rel":"stylesheet" })
        
        ctx = { 'theme': theme, "styles": styles }
        return render_to_string("xadrpy/themes/styles.html", ctx, context)

class ScriptsNode(XWidgetBase):

    def value(self, context, *args, **kwargs):
        theme = getattr(context.get('request', object), "theme", None)
        TEMPLATE = kwargs.pop("TEMPLATE", None)
        if not theme and not TEMPLATE:
            return ""
        if not theme:
            return TEMPLATE.render(context)

        ctx = { 
            'theme': theme,
        }
        return render_to_string("xadrpy/themes/scripts.html", ctx, context)

register.widget('theme_styles')(StylesNode)
register.widget('theme_scripts')(ScriptsNode)

