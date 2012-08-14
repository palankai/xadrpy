from django.conf import settings
from xadrpy.core.i18n import conf as i18n_conf
from django.utils.translation import ugettext_lazy as _
import os
from threading import local

_local = local()


DEFAULT_SITE_ID = getattr(settings, 'SITE_ID')
LANGUAGE_CODE_KWARG = i18n_conf.LANGUAGE_CODE_KWARG

TOUCH_WSGI_FILE = True

WSGI_PATH = getattr(settings, u'WSGI_PATH', os.environ.get('WSGI_PATH', None))
APPLICATIONS = getattr(settings, "APPLICATIONS", {})

META_HANDLER = "xadrpy.router.libs.MetaHandler"

META_HANDLER_CLS = None

VERSION = 1

RELATIVE_FROM = (
    ('absolute', _("Absolute path")),
    ('settings', _("location of settings.py")),
    ('document', _("document root")),
    
)