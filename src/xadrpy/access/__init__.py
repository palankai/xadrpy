from models import prefs, prefs_set, prefs_drop, prefs_get, prefs_find
from xadrpy.management.libs import SubCommand
__ALL__ = ['prefs', 'prefs_set', 'prefs_drop', 'prefs_find']

class Prefs(SubCommand):
    
    def register(self):
        _get = self.command.add_subcommand(self.handle, "prefs", help="get prefs")
        _del = self.command.add_subcommand(self.handle, "prefs.del", help="delete pref")
        _set = self.command.add_subcommand(self.handle, "prefs.set", help="set pref value")
        _list = self.command.add_subcommand(self.handle, "prefs.list", help="list prefs")

        self.add_arguments(_get)
        self.add_arguments(_del)
        self.add_set_arguments(_set)
        self.add_arguments(_list)
    
    def add_arguments(self, subcommand):
        subcommand.add_argument("key", help="Key of prefs value")
        subcommand.add_argument("--namespace", action="store", help="Namespace", dest="namespace", metavar="name")
        subcommand.add_argument("--site", action="store", help="Site id or domain", dest="site", metavar="site")
        subcommand.add_argument("--user", action="store", help="User id or name", dest="user", metavar="user")
        subcommand.add_argument("--lang", action="store", help="Language code", dest="language_code", metavar="language")

    def add_set_arguments(self, subcommand):
        subcommand.add_argument("key", help="Key of prefs value")
        subcommand.add_argument("--namespace", action="store", help="Namespace", dest="namespace", metavar="name")
        subcommand.add_argument("--site", action="store", help="Site id or domain", dest="site", metavar="site")
        subcommand.add_argument("--user", action="store", help="User id or name", dest="user", metavar="user")
        #lang_grp = subcommand.add_mutually_exclusive_group()
        subcommand.add_argument("--lang", action="store", help="Language code", dest="language_code", metavar="language")
        subcommand.add_argument("--trans", action="store", help="Translation language code", dest="translation_language_code", metavar="language")
        subcommand.add_argument("-j","--json", action="store_true", help="Value is json string", dest="is_json")
        subcommand.add_argument("-f","--file", action="store_true", help="File containing value", dest="is_file")
        subcommand.add_argument("value", action="store", help="Value", metavar="value")
    
    def handle(self, **kwargs):
        print kwargs
        pass
