'''
Created on 2012.07.31.

@author: pcsaba
'''
from django.core.management.base import NoArgsCommand, CommandError
from xadrpy.router.base import update_signatures

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        self.stdout.write('Updating signatures...\n')
        try:
            update_signatures()
        except Exception, e:
            raise CommandError(e)
        self.stdout.write('done.\n')
