from xadrpy.utils.jsonlib import JSONEncoder
from django.utils.safestring import mark_safe
from xadrpy.core.templates.base import WidgetLibrary, XWidgetBase
from django.utils import importlib
register = WidgetLibrary()

@register.filter
def JSON(value):
    return mark_safe(JSONEncoder().encode(value))

class XWidgetNode(XWidgetBase):

    def value(self, context, name, *args, **kwargs):
        module_name, widget_name = name.rsplit(".",1)
        module = importlib.import_module(module_name)
        widget = getattr(module, widget_name)
        try:
            return widget(context, *args, **kwargs)
        except Exception, e:
            return "Exception: %s" % e

register.widget('xwidget')(XWidgetNode)

