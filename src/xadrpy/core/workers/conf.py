from django.conf import settings

CONTAINERS = getattr(settings, "WORKER_CONTAINERS", [])