from django.conf import settings

COMMON_PREFERENCES = getattr(settings, "PREFERENCES", ())
