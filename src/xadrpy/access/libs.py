from xadrpy.management.libs import SubCommand
import imp
import conf
from models import Property
from django.conf import settings
from django.utils import importlib
from django.core.management.base import CommandError

class PrefsCommands(SubCommand):
    
    def register(self):
        _get = self.command.add_subcommand(self.handle, "prefs", help="get prefs")
        _init = self.command.add_subcommand(self.init, "prefs.init", help="Collecting initial preferences")
        _reset = self.command.add_subcommand(self.reset, "prefs.reset", help="Reset initial preferences")

        self.add_arguments(_get)
    
    def add_arguments(self, subcommand):
        subcommand.add_argument("key", metavar="key", help="Key of prefs value")
        subcommand.add_argument("--namespace", action="store", help="Namespace", dest="namespace", metavar="name")
        subcommand.add_argument("--site", action="store", help="Site id or domain", dest="site", metavar="site")
        subcommand.add_argument("--user", action="store", help="User id or name", dest="user", metavar="user")
        subcommand.add_argument("--lang", action="store", help="Language code", dest="language_code", metavar="language")
        subcommand.add_argument("--delete", action="store_true", help="Delete", dest="delete")
        subcommand.add_argument("--trans", action="store", help="Translation language code", dest="translation_language_code", metavar="language")
        subcommand.add_argument("--value", action="store", help="Value", metavar="value")
        subcommand.add_argument("-j","--json", action="store_true", help="Value is json string", dest="is_json")
        subcommand.add_argument("-f","--file", action="store_true", help="File containing value", dest="is_file")

    def handle(self, **kwargs):
        raise CommandError("Not implemented jet")

    
    def reset(self, **kwargs):
        Property.objects.all().delete()
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
            instance=preference.get("instance",None) 
            site=preference.get("site",None) 
            consumer=preference.get("consumer",None)
            role=preference.get("role",None) 
            namespace=preference.get("namespace",None)
            key=preference.get("key",None)
            language_code=preference.get("language_code",None)
            
            value=preference.get("value", None) 
            vtype=preference.get("vtype", None) 
            title=preference.get("title", None)
            description=preference.get("description", None)
            meta=preference.get("meta", None)
            status=preference.get("status", 1)
            init=preference.get("init", False)
            debug=preference.get("debug", False)
            trans=preference.get("trans", {})
            
            k = {'instance': instance, 'site': site, 'consumer': consumer, 'role': role, 'namespace': namespace, 'key': key, 'language_code': language_code}
            v = {'value': value, 'vtype': vtype, 'title': title, 'description': description, 'meta': meta, 'status': status, 'init': init, 'debug': debug, 'trans': trans, 'source': source}
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
        
        for preference in conf.PREFERENCES:
            process_preference(preferences, preference, "settings")
        
        for kwargs in preferences.values():
            Property.objects.init_by(**kwargs)
    
