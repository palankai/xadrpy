from django.conf import settings

# admin: when staff logged in
# admin-cookie: when staff logged in, and cookie set
# always: show always

MODE = getattr(settings, "TOOLBAR_MODE", "admin")
COOKIE = getattr(settings, 'TOOLBAR_COOKIE', 'x-toolbar')

STATIC_URL = getattr(settings, "STATIC_URL")
