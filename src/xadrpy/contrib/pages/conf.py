from django.conf import settings
from django.utils.translation import ugettext_lazy as _

DEFAULT_TEMPLATE = getattr(settings, "PAGES_DEFAULT_TEMPLATE", "xadrpy/pages/page.html")
DEFAULT_VIEW = getattr(settings, 'PAGES_DEFAULT_VIEW', 'xadrpy.contrib.pages.views.page')

TEMPLATES = getattr(settings, 'PAGES_TEMPLATES', ((DEFAULT_TEMPLATE, _("Base template")),))

PAGE_STATES = (
    ('DRA', _('Draft')),
    ('PUB', _('Published')),
    ('HID', _('Hidden')),
)

PREFERENCES = (
)