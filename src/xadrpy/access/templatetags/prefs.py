from xadrpy.templates.lib import XWidgetBase, WidgetLibrary
from xadrpy.access import prefs


register = WidgetLibrary()


class PropertyNode(XWidgetBase):

    def value(self, context, key=None, default=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, trans=None, order=""):
        order = [item.strip() for item in order.split(",") if item.strip()]
        v = prefs(key=key, default=default, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom=custom, namespace=namespace, language_code=language_code, trans=trans, order=order)
        if not self.asvar:
            v = v or ""
        return v 
            

register.widget('prefs')(PropertyNode)


