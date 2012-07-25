from xadrpy.templates.lib import XWidgetBase, WidgetLibrary
from xadrpy.auth.models import Property
from xadrpy.auth import prefs


register = WidgetLibrary()


class PropertyNode(XWidgetBase):

    def value(self, context, key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, default=None, trans=None, order=""):
        order = [item.strip() for item in order.split(",") if item.strip()]
        v = prefs(key=key, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom=custom, namespace=namespace, language_code=language_code, default=default, trans=trans, order=order)
        if not self.asvar:
            v = v or ""
        return v 
            

register.widget('prefs')(PropertyNode)


