from models import Pref
from xadrpy.management.libs import SubCommand
import imp
import conf
from django.conf import settings
from django.utils import importlib
from django.core.management.base import CommandError

def prefs(key=None, default=None, site=None, group=None, user=None, namespace=None, language_code=None, trans=None, order=[]):
    kwargs = {
        'key':key,
        'site':site, 
        'group':group, 
        'user':user, 
        'namespace':namespace,
        'language_code':language_code,
    }
    pref=Pref.objects.get_by(**kwargs)
    while not pref and len(order):
        kwargs.pop(order.pop())
        pref=Pref.objects.get_by(**kwargs)
    return pref and pref.get_value(language_code=trans) or default

def prefs_set(value, key=None, site=None, group=None, user=None, namespace=None, language_code=None):
    pref, unused = Pref.objects.get_or_create_by(key=key, site=site, group=group, user=user, namespace=namespace, language_code=language_code)
    pref.value = value
    pref.save()
    return prefs

def prefs_drop(key=None, site=None, group=None, user=None, namespace=None, language_code=None):
    try:
        pref = Pref.objects.get_by(key=key, site=site, group=group, user=user, namespace=namespace, language_code=language_code)
        pref.delete()
        return True
    except Pref.DoesNotExist:
        return False

class PrefsCommands(SubCommand):
    
    def register(self):
        _get = self.command.add_subcommand(self.handle, "prefs", help="get prefs")
        _init = self.command.add_subcommand(self.init, "prefs.init", help="Collecting initial preferences")
        _reset = self.command.add_subcommand(self.reset, "prefs.reset", help="Reset initial preferences")

        self.add_arguments(_get)
    
    def add_arguments(self, subcommand):
        subcommand.add_argument("key", metavar="key", help="Key of prefs value")
        subcommand.add_argument("--site", action="store", help="Site id or domain", dest="site", metavar="site")
        subcommand.add_argument("--group", action="store", help="Group id or name", dest="group", metavar="group")
        subcommand.add_argument("--user", action="store", help="User id or name", dest="user", metavar="user")
        subcommand.add_argument("--namespace", action="store", help="Namespace", dest="namespace", metavar="name")
        subcommand.add_argument("--lang", action="store", help="Language code", dest="language_code", metavar="language")

        subcommand.add_argument("--delete", action="store_true", help="Delete", dest="delete")
        subcommand.add_argument("--trans", action="store", help="Translation language code", dest="translation_language_code", metavar="language")
        subcommand.add_argument("--value", action="store", help="Value", metavar="value")
        subcommand.add_argument("-j","--json", action="store_true", help="Value is json string", dest="is_json")
        subcommand.add_argument("-f","--file", action="store_true", help="File containing value", dest="is_file")

    def handle(self, **kwargs):
        raise CommandError("Not implemented jet")

    
    def reset(self, **kwargs):
        Pref.objects.all().delete()
        self.init(**kwargs)
    
    def init(self, **kwargs):
        """
        Collect preferences from settings, confs
        """
        def hash_for_dict(d):
            """
            Generate an easy hash for a simple dict
            :param d: a dict
            """
            return ";".join(["%s:%s" % (k,v) for k,v in d.items()])
        
        def process_preference(preferences, preference, source):
            """
            Process a preference
            
            :param preferences: common preferences dict
            :param preference: simple dict
            """
            key=preference.get("key",None)
            site=preference.get("site",None) 
            group=preference.get("group",None) 
            user=preference.get("user",None) 
            namespace=preference.get("namespace",None)
            language_code=preference.get("language_code",None)
            
            value=preference.get("value", None) 
            meta=preference.get("meta", {})
            trans=preference.get("trans", {})
            
            k = {'site': site, 'group':group, 'user':user, 'namespace': namespace, 'key': key, 'language_code': language_code}
            v = {'value': value, 'meta': meta, 'trans': trans}
            v.update(k)
            h = hash_for_dict(k)
            if h in preferences:
                preferences[h].update(v)
            else:
                preferences[h]=v
    
        preferences = dict()
    
        for app in settings.INSTALLED_APPS:
    
            try:
                app_path = importlib.import_module(app).__path__
            except AttributeError:
                continue
    
            try:
                imp.find_module('conf', app_path)
            except ImportError:
                continue
            conf_module_name = "%s.conf" % app
            module = importlib.import_module(conf_module_name)
            PREFERENCES = getattr(module, "PREFERENCES", ())
    
            for preference in PREFERENCES:
                process_preference(preferences, preference, conf_module_name)
        
        for preference in conf.COMMON_PREFERENCES:
            process_preference(preferences, preference, "settings")
        
        for kwargs in preferences.values():
            Pref.objects.init_by(**kwargs)
    
