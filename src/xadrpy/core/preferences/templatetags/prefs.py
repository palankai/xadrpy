from xadrpy.templates.libs import XWidgetBase, WidgetLibrary
from xadrpy.core.preferences.libs import prefs


register = WidgetLibrary()


class PropertyNode(XWidgetBase):

    def value(self, context, key=None, default=None, site=None, group=None, user=None, namespace=None, language_code=None, trans=None, order=""):
        order = [item.strip() for item in order.split(",") if item.strip()]
        v = prefs(key=key, default=default, site=site, group=group, user=user, namespace=namespace, language_code=language_code, trans=trans, order=order)
        if not self.asvar:
            v = v or ""
        return v 
            

register.widget('prefs')(PropertyNode)


