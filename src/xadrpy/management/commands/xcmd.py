'''
Created on 2012.08.02.

@author: pcsaba
'''
from django.core.management.base import BaseCommand, CommandError
import argparse
import traceback
import sys
from django.utils.encoding import smart_str
from xadrpy.management.libs import is_application_installed
from xadrpy import conf

class MyHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog,
                 indent_increment=2,
                 max_help_position=40,
                 width=120):
        super(MyHelpFormatter, self).__init__(prog, indent_increment=2, max_help_position=40, width=120)

def test_func(**kwargs):
    print kwargs

class Command(BaseCommand):
    
    description = "xadrpy console tools"
    prog = "manage.py xcmd"
    need_subcommands = True
    subcommands_title = "Subcommands"
    subcommands_description = None
    subcommands_metavar = "subcommand"
    shift = 2
    language_code = "en-us"
    
    def __init__(self):
        BaseCommand.__init__(self)
        self.parser = argparse.ArgumentParser(description='xadrpy\n console tools',
                                         prog="manage.py xcmd",
                                         #usage="manage.py xcmd [options] subcommand",
                                         formatter_class=MyHelpFormatter)
        self.init_default_arguments()
        self.subcommands = None
        if self.need_subcommands:
            self.subcommands = self.parser.add_subparsers(title=self.subcommands_title, 
                                                          description=self.subcommands_description, 
                                                          metavar=self.subcommands_metavar)
            self.init_subcommands()

    def init_default_arguments(self):
        self.parser.add_argument("-v","--verbosity", action="store", metavar="VERBOSITY", choices=[0,1,2,3], type=int, help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output")
        self.parser.add_argument("--settings", help='The Python path to a settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.')
        self.parser.add_argument("--pythonpath", help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".')
        self.parser.add_argument("--traceback", action="store_true", help='Print traceback on exception')
    
    def init_subcommands(self):
        #self.add_subcommand(test_func, "themes.collect", help="collect themes",  description="collecting themes")
        from xadrpy.management.libs import GeneralCommands
        general = GeneralCommands(self)
        general.register()

        if is_application_installed("xadrpy.core.preferences"):
            from xadrpy.core.preferences.libs import PrefsCommands
            commands = PrefsCommands(self)
            commands.register()
            general.add_commands(commands, "preferences")

        if is_application_installed("xadrpy.core.router"):
            from xadrpy.core.router.libs import RouterCommands
            commands = RouterCommands(self)
            commands.register()
            general.add_commands(commands, "router")

        if is_application_installed("xadrpy.contrib.plugins"):
            from xadrpy.contrib.plugins.libs import PluginsCommands
            commands = PluginsCommands(self)
            commands.register()
            general.add_commands(commands, "plugins")
        
        if is_application_installed("xadrpy.contrib.themes"):
            from xadrpy.contrib.themes.libs import ThemesCommands
            commands = ThemesCommands(self)
            commands.register()
            general.add_commands(commands, "themes")
            

        if is_application_installed("xadrpy.contrib.entries"):
            from xadrpy.contrib.entries import EntriesCommands
            commands = EntriesCommands(self)
            commands.register()
            general.add_commands(commands, "entries")

    
    def print_header(self):
        self.stdout.write("xadrpy %s - django toolkit\n" % conf.VERSION)
        self.stdout.write("Author Csaba Palankai <csaba.palankai@gmail.com>\n")
        
    def add_subcommand(self, subcommand, name, help=None, description=None, epilog=None, prog=None, usage=None):
        parser = self.subcommands.add_parser(name, help=help, description=description, epilog=epilog, prog=prog, usage=usage)
        parser.set_defaults(subcommand=subcommand)
        return parser
    
    def run_from_argv(self, argv):
        namespace = self.parser.parse_args(argv[self.shift:])
        kwargs = namespace.__dict__.copy()
        kwargs.pop(self.subcommands_metavar)
        kwargs.pop("settings")
        kwargs.pop("pythonpath")
        kwargs.pop("traceback")
        if 'verbosity' in kwargs and kwargs['verbosity']==None:
            kwargs.pop("verbosity")
        show_traceback = kwargs.get('traceback', False)
        saved_lang = None

        if self.can_import_settings:
            try:
                from django.utils import translation
                saved_lang = translation.get_language()
                translation.activate(self.language_code)
            except ImportError, e:
                # If settings should be available, but aren't,
                # raise the error and quit.
                if show_traceback:
                    traceback.print_exc()
                else:
                    sys.stderr.write(smart_str(self.style.ERROR('Error: %s\n' % e)))
                sys.exit(1)

        try:
            self.stdout = kwargs.get('stdout', sys.stdout)
            self.stderr = kwargs.get('stderr', sys.stderr)
            if self.requires_model_validation:
                self.validate()
            
            output = namespace.subcommand(**kwargs)
            if output:
                if self.output_transaction:
                    # This needs to be imported here, because it relies on
                    # settings.
                    from django.db import connections, DEFAULT_DB_ALIAS
                    connection = connections[kwargs.get('database', DEFAULT_DB_ALIAS)]
                    if connection.ops.start_transaction_sql():
                        self.stdout.write(self.style.SQL_KEYWORD(connection.ops.start_transaction_sql()) + '\n')
                self.stdout.write(output)
                if self.output_transaction:
                    self.stdout.write('\n' + self.style.SQL_KEYWORD("COMMIT;") + '\n')
        except CommandError, e:
            if show_traceback:
                traceback.print_exc()
            else:
                self.stderr.write(smart_str(self.style.ERROR('Error: %s\n' % e)))
            sys.exit(1)
        if saved_lang is not None:
            translation.activate(saved_lang)
