# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.conf.urls import patterns
from django.utils.translation import get_language
from django.core.urlresolvers import RegexURLResolver
import conf

def i18n_patterns(prefix, *args):
    """
    Adds the language code prefix to every URL pattern within this
    function. This may only be used in the root URLconf, not in an included
    URLconf.
    Fontos: Ez a függvény az eredetitől annyiban tér el, hogy saját
    LocaleRegexURLResolver-t ad vissza! 

    """
    pattern_list = patterns(prefix, *args)
    if not settings.USE_I18N:
        return pattern_list
    return [LocaleRegexURLResolver(pattern_list)]


class LocaleRegexURLResolver(RegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    
    Bővített: Configurációs opciótól függően, az alapértelmezett nyelvnél
    le lehet tiltani, hogy prefixel jelenjen meg!
    """
    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        super(LocaleRegexURLResolver, self).__init__(
            None, urlconf_name, default_kwargs, app_name, namespace)

    @property
    def regex(self):
        language_code = get_language()
        if not conf.NEED_PREFIX_TO_DEFAULT_LANGUAGE and settings.LANGUAGE_CODE == language_code:
            return re.compile(u"")
        if language_code not in self._regex_dict:
            regex_compiled = re.compile('^%s/' % language_code, re.UNICODE)
            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]
