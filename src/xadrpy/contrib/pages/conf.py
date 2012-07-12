from django.conf import settings
from django.utils.translation import ugettext_lazy as _

TEMPLATES = getattr(settings, 'PAGES_TEMPLATES', (("page.html", _("Base template")),))
