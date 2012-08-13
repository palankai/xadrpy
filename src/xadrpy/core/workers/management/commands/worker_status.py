from django.core.management.base import BaseCommand
from xadrpy.core.workers.daemon import DaemonHandler

class Command(BaseCommand):
    
    def handle(self, *worker_list, **options):
        daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
        daemon_handler.status()
    