from django.core.management.base import NoArgsCommand, CommandError
import signal
import time
import os
import sys
from xadrpy.workers.daemon import Daemon, DaemonHandler

class Command(NoArgsCommand):
    
    def handle(self, **options):
        daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
        try:
            daemon_handler.stop()
            sys.stdout.write("Worker is stopped.\n")
        except Exception, e:
            sys.stderr.write(str(e)+"\n")
        
