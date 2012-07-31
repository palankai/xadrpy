from django.conf import settings
from xadrpy.i18n import conf as i18n_conf
import os

DEFAULT_SITE_ID = getattr(settings, 'SITE_ID')
LANGUAGE_CODE_KWARG = i18n_conf.LANGUAGE_CODE_KWARG

TOUCH_WSGI_FILE = True

WSGI_PATH = getattr(settings, u'WSGI_PATH', os.environ.get('WSGI_PATH', None))

META_HANDLER = "xadrpy.router.libs.MetaHandler"

META_HANDLER_CLS = None

VERSION = 1