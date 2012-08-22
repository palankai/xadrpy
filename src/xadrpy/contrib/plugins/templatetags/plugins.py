from xadrpy.core.templates.base import XWidgetBase, WidgetLibrary
from xadrpy.contrib.plugins.models import PluginStore, PluginPlace
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger("xadrpy.contrib.plugins.templatetags.plugins")

register = WidgetLibrary()

class PluginNode(XWidgetBase):

    def value(self, context, name, *args, **kwargs):
        placeholder = kwargs.get('placeholder', None)
        template = kwargs.pop('TEMPLATE', None)
        request = context['request']
        try:
            store = PluginStore.objects.get_plugin(name)
            if not store.enabled:
                return
            plugin_cls = store.get_plugin_cls()
            plugin = store.get_instance(*args, **kwargs)
            if placeholder:
                model = plugin_cls.model or PluginPlace
                place, unused = model.objects.get_or_create(store=store, placeholder=placeholder)
                if not place.enabled:
                    return
                plugin.set_place(place)
        except PluginStore.DoesNotExist, e:
            logger.exception("Plugin not found in the store")
            raise
        except ImproperlyConfigured, e:
            logger.exception("Plugin class not found")
            raise
        except Exception, e:
            logger.exception(e)
            raise
        plugin.init_inline(template)
        request.xtensions.append(plugin)
        #plugin.init_template(template)
        context_len = len(context.dicts)
        try:
            plugin.init(context)
            if plugin.is_visible():
                return plugin.render(context)
            else:
                return ""
        except Exception, e:
            logger.exception("Plugin '%s' (placeholder=%s) render error: %s", name, placeholder, e)
            return "Plugin exception: %s" % e
        finally:
            while len(context.dicts)>context_len: context.pop()

register.widget('plugin')(PluginNode)
