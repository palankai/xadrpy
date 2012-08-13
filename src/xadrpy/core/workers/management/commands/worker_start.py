from django.core.management.base import NoArgsCommand, CommandError
from xadrpy.core.workers.daemon import DaemonHandler

class Command(NoArgsCommand):
    
    def handle(self, **options):
        daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
        try:
            daemon_handler.start()
        except Exception, e:
            raise CommandError(e)
