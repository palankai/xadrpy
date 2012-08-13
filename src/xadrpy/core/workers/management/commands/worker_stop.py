from django.core.management.base import NoArgsCommand, CommandError
import sys
from xadrpy.core.workers.daemon import DaemonHandler

class Command(NoArgsCommand):
    
    def handle(self, **options):
        daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
        try:
            daemon_handler.stop()
            sys.stdout.write("Worker is stopped.\n")
        except Exception, e:
            raise CommandError(e)
        
