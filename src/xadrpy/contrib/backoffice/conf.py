from django.conf import settings
TITLE = getattr(settings, "BACKOFFICE_TITLE","BackOffice")
DESCRIPTION = getattr(settings, "BACKOFFICE_TITLE","BackOffice System")

NAMESPACES = {}

CONTROLLERS = [
    'backoffice.controller.MainMenu',
]

STORES = []