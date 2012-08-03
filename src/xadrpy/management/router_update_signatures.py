from django.core.management.base import NoArgsCommand, CommandError
from xadrpy.management import libs
from xadrpy.router.base import update_signatures
from xadrpy.conf import VERSION

#from xadrpy.router.management.commands.update_signatures import Command

#class Command(NoArgsCommand):
#    
#    help = 'Updates all router objects signature'
#    requires_model_validation = True
#    
#    def handle_noargs(self, **options):
#        libs.test_is_application_installed("xadrpy.router")
#        self.stdout.write('Updating signatures...\n')
#        try:
#            update_signatures()
#        except Exception, e:
#            raise CommandError(e)
#        self.stdout.write('done.\n')
#
#    def get_version(self):
#        return "xadrpy-%s" % VERSION
