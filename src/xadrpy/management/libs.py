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
        
    def print_header(self):
        self.command.print_header()
        self.stdout.write("\n")
        
    def register(self):
        pass
    
