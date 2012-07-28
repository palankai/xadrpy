from xadrpy.templates.libs import WidgetLibrary, XWidgetBase
from django.template.loader import render_to_string
register = WidgetLibrary()

class StylesNode(XWidgetBase):

    def value(self, context, *args, **kwargs):
        theme = getattr(context.get('request', object), "theme", None)
        TEMPLATE = kwargs.pop("TEMPLATE", None)
        if not theme and not TEMPLATE:
            return ""
        if not theme:
            return TEMPLATE.render(context)
        ctx = { 'theme': theme }
        return render_to_string("xadrpy/themes/styles.html", ctx, context)

class ScriptsNode(XWidgetBase):

    def value(self, context, *args, **kwargs):
        theme = getattr(context.get('request', object), "theme", None)
        TEMPLATE = kwargs.pop("TEMPLATE", None)
        if not theme and not TEMPLATE:
            return ""
        if not theme:
            return TEMPLATE.render(context)
        ctx = { 'theme': theme }
        return render_to_string("xadrpy/themes/scripts.html", ctx, context)

register.widget('theme_styles')(StylesNode)
register.widget('theme_scripts')(ScriptsNode)
