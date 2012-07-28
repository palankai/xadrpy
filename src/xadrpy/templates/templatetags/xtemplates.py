from xadrpy.utils.jsonlib import JSONEncoder
from django.utils.safestring import mark_safe
from xadrpy.templates.libs import WidgetLibrary, XWidgetBase
from django.utils import importlib
from xadrpy.templates.libs import PLUGIN_CACHE
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

class PluginNode(XWidgetBase):

    def value(self, context, name, placeholder, *args, **kwargs):
        if name in PLUGIN_CACHE:
            plugin = PLUGIN_CACHE[name]
        else:
            try:
                module_name, widget_name = name.rsplit(".",1)
                module = importlib.import_module(module_name)
                plugin = getattr(module, widget_name)
            except:
                raise Exception("Plugin error - maybe undefinded plugin or holder module not in INSTALLED_APPS")
        try:
            plugin_instance = plugin(placeholder)
            plugin_instance.init_template(kwargs.pop('TEMPLATE', None))
            return plugin_instance.render(context, *args, **kwargs)
        except Exception, e:
            return "Exception: %s" % e

register.widget('plugin')(PluginNode)