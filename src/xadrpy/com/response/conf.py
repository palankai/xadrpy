from django.conf import settings

EXCEPTION_RESPONSE_NEED_STACK = getattr(settings, "XADRPY_EXCEPTION_RESPONSE_NEED_STACK", getattr(settings, "DEBUG", False))
JSON_MIMETYPE = getattr(settings, "XADRPY_JSON_MIMETYPE", "application/json")
DEFAULT_JSON_RESPONSE = getattr(settings, "XADRPY_DEFAULT_JSON_RESPONSE", "base")