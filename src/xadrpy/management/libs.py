from django.conf import settings
from django.core.management.base import CommandError
from django.utils.translation import ugettext as _


def test_is_application_installed(app_name):
    if not is_application_installed(app_name):
        raise CommandError(_("The '%(app_name)s' app is listed in settings.INSTALLED_APPS") % {"app_name":app_name} )

def is_application_installed(app_name):
    return app_name in settings.INSTALLED_APPS


class SubCommand(object):
    
    def __init__(self, command):
        self.command = command

    def get_stdout(self):
        return self.command.stdout
    stdout = property(get_stdout)

    def get_stderr(self):
        return self.command.stderr
    stderr = property(get_stderr)
        
    def register(self):
        pass

    def reset(self, **kwargs):
        pass

    def init(self, **kwargs):
        pass
    
    
class GeneralCommands(SubCommand):
    
    def __init__(self, command):
        super(GeneralCommands, self).__init__(command)
        self.commands = []
    
    def register(self):
        _init = self.command.add_subcommand(self.init, "general.init", help="General init - run all inits")
        _reset = self.command.add_subcommand(self.reset, "general.reset", help="General reset - run all resets")
    
    def add_commands(self, commands, title):
        self.commands.append((commands, title))
    
    def init(self, **kwargs):
        for commands, title in self.commands:
            self.stdout.write("init %s...\n" % title)
            commands.init(**kwargs)
    
    def reset(self, **kwargs):
        for commands, title in self.commands:
            self.stdout.write("reset %s...\n" % title)
            commands.reset(**kwargs)
