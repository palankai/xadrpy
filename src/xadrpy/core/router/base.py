from django.utils import translation
from django.utils.functional import lazy
import conf
from xadrpy.core.i18n.utils import i18n_patterns
from django.conf.urls import patterns
from xadrpy.core.preferences.base import Prefs
from xadrpy.utils.key_string import key_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from xadrpy.contrib.toolbar.base import ToolbarButton, ToolbarSwitch
import logging
logger = logging.getLogger("xadrpy.core.route.base")

def get_local_request():
    return getattr(conf._local, "request", None)

class RoutePrefs(Prefs):

    def __init__(self, instance, store, **opts):
        self.route = instance
        self.parent = instance.get_parent() and instance.get_parent().prefs
        self.master = instance.get_master() and instance.get_master().prefs
        try:
            self.translated = self.route.translation(get_or_create=False).meta
        except ObjectDoesNotExist:
            self.translated = None
        super(RoutePrefs, self).__init__(instance, store, **opts)

    def get(self, key, default=None):
        value = super(RoutePrefs, self).get(key)
        if value is None and self.master:
            value = self.master.get(key)
        if value is None and self.parent:
            value = self.parent.get(key)
        if value is None:
            return default
        return value

    def tget(self, key, default=None):
        if self.has_getter(key, translated=True):
            return self.getter(key, translated=True)
        value = self._tget(key)
        if value is None and self.master:
            value = self.master.tget(key)
        if value is None and self.parent:
            value = self.parent.tget(key)
        if value is None:
            return default
        return value

    def _tget(self, key):
        value = super(RoutePrefs, self).get(key)
        if value is None: return None
        if not self.translated:
            return value
        tvalue = key_string(self.translated, key)
        if tvalue is not None:
            return tvalue
        return value

    def get_menu_title(self, **opts):
        return self.translated.get('menu_title') or self.route.get_title()

    def get_meta_title(self, **opts):
        if self.store.get("overwrite_meta_title") and self.store.get("meta_title"):
            return self.translated.get("meta_title") or self.store.get("meta_title") or self.route.get_title()

        self_title = self.translated.get("meta_title") or self.store.get("meta_title") or self.route.get_title()
        if self.parent and self.parent.get_meta_title(**opts):
            self_title = self_title + " | " + self.parent.get_meta_title(**opts)
        return self_title

    def get_meta_keywords(self, **opts):
        meta_keywords = self.store.get('meta_keywords')
        if meta_keywords: return meta_keywords
        return self.parent and self.parent.get_meta_keywords(**opts) or ""

    def get_meta_description(self, **opts):
        meta_description = self.store.get("meta_description")
        if meta_description: return meta_description
        return self.parent and self.parent.get_meta_description(**opts) or ""


class Application(object):

    title = None

    def __init__(self, route, **opts):
        self.route = route
        self.parent = route.get_parent() and route.get_parent().app
        self.master = route.get_master() and route.get_master().app

    def get_absolute_url(self):
        pass

    def get_translated_regex(self, postfix="$", slash="/"):
        return self.get_regex(postfix=postfix, slash=slash, language_code=translation.get_language())
    get_translated_regex = lazy(get_translated_regex, unicode)


    def get_regex(self, postfix="$", slash="/", language_code=None):
        regex = self.get_regex_base(postfix, slash, language_code)
        slug = self.route.get_slug(language_code)
        if len(slug):
            return regex + slug + slash + postfix
        return regex + postfix

    def get_regex_base(self, postfix="$", slash="/", language_code=None):
        if self.route.parent:
            return self.parent.get_regex(postfix="", slash="/", language_code=language_code)
        if self.route.language_code: #FIXME: and (NEED_PREFIX_TO_DEFAULT_LANGUAGE or self.route.language_code != settings.language_code):
            return "^%s/" % self.route.language_code
        return "^"

    def append_pattern(self, url_patterns):
        if not self.route.enabled:
            return
        root_language_code = self.get_root_language_code()
        kwargs = root_language_code and {conf.LANGUAGE_CODE_KWARG: root_language_code} or {}
        kwargs.update({'route_id': self.route.id})
        urls = self.get_urls(kwargs)
        if not urls: return
        url_patterns += self.patterns('', *urls)

    def get_urls(self, kwargs):
        return []

    def patterns(self, *args, **kwargs):
        if not self.parent and self.route.i18n:
            return i18n_patterns(*args, **kwargs)
        return patterns(*args, **kwargs)

    def get_root_language_code(self):
        return self.route.get_root().language_code

    def get_context(self, request, *args, **kwargs):
        return {}

    def toolbar_setup(self, context, toolbar, allow_subpage=True):
        from django.core.urlresolvers import reverse
        from django.conf import settings
        request = context['request']
        toolbar.title = self.title
        btn_move = ToolbarButton(_("Move"), "#")

        if self.route.route_ptr.get_previous_sibling():
            forward_url = reverse("admin:x-router-route-admin-forward", kwargs={'pk': self.route.id}) + "?next=" + request.get_full_path()
            btn_move.menu.append(ToolbarButton(_("Move forward"), forward_url))
        if self.route.route_ptr.get_next_sibling():
            backward_url = reverse("admin:x-router-route-admin-backward", kwargs={'pk': self.route.id}) + "?next=" + request.get_full_path()
            btn_move.menu.append(ToolbarButton(_("Move backward"), backward_url))
        toolbar.add(btn_move)

        info = self.route._meta.app_label, self.route._meta.module_name
        window = {"width": 1020, "height": 650, "toolbar": 0, "titlebar":0, "status":0, "resizable":1, "scrollbars":1, "location":0, "left":'auto' }

        change_url = "%s?_popup=1&from-toolbar=1" % (reverse("admin:%s_%s_change" % info, args=[self.route.id]))
        btn_edit = ToolbarButton(_("Edit page"), change_url, name="x-page-editor", opts=window)
        delete_url = reverse("admin:x-%s-%s-admin-delete" % info, kwargs={'pk': self.route.id}) + "?next=/"
        btn_edit.menu.append(ToolbarButton(_("Delete"), delete_url, question="Do you want to delete this page?"))
        toolbar.add(btn_edit)



        btn_new = ToolbarButton(_("New page"), "#", name="x-page-editor", opts=window)
        btn_sub = ToolbarButton(_("New subpage"), "#", name="x-page-editor", opts=window)
        for name, route in settings.ROUTES:
            n = ToolbarButton(route.get('title'), "#")
            s = ToolbarButton(route.get('title'), "#")
            btn_new.menu.append(n)
            btn_sub.menu.append(s)
            for key, label in route['applications']:
                add_url = "%s?_popup=1&from-toolbar=1&parent=%s&application_name=%s" % (reverse("admin:%s_%s_add" % route.get('admin')), self.route.parent.id if self.route.parent else "", key)
                add_sub_url = "%s?_popup=1&from-toolbar=1&parent=%s&application_name=%s" % (reverse("admin:%s_%s_add" % route.get('admin')), self.route.id, key)
                n.menu.append(ToolbarButton(label, add_url, name="x-page-editor", opts=window))
                s.menu.append(ToolbarButton(label, add_sub_url, name="x-page-editor", opts=window))

        toolbar.append_switch(ToolbarSwitch("edit", _("Edit mode"), False, [(True, _("On")), (False, _("Off"))]))
        toolbar.append_switch(ToolbarSwitch("preview", _("Preview mode"), False, [(True, _("On")), (False, _("Off"))]))

        toolbar.add(btn_new)
        if allow_subpage:
            toolbar.add(btn_sub)



