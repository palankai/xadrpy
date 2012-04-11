from django.conf import settings

SESSION_KEY = 'PermanentSessionId'
REQUEST_KEY = 'permanent_session'

DEFAULT_TIMEOUT = getattr(settings, "XADRPY_PERMANENT_SESSION_DEFAULT_TIMEOUT", 300)

