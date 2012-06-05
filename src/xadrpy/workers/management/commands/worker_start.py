from django.core.management.base import NoArgsCommand, CommandError
from xadrpy.workers.worker import Worker
import sys
from xadrpy.workers import lib
from xadrpy.workers.exceptions import InvalidContainerName
from xadrpy.workers.daemon import Daemon, DaemonHandler
from xadrpy.workers.conf import CONTAINERS

class Command(NoArgsCommand):
    
    def handle(self, **options):
        daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
        try:
            daemon_handler.start()
        except Exception, e:
            sys.stderr.write(str(e)+"\n")
