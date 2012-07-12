from django.conf import settings
from django.utils.translation import ugettext_lazy as _

TEMPLATES = getattr(settings, 'PAGES_TEMPLATES', (("page.html", _("Base template")),))

RESOLVE_NORMAL = '(?P<slug>[0-9a-zA-Z\-/_]+)'
RESOLVE_YEAR_BASED = '(?P<year>[0-9]{4})(/(?P<slug>[0-9a-zA-Z\-/_]+))?'
RESOLVE_MONTH_BASED = '(?P<year>[0-9]{4})(/(?P<month>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?'
RESOLVE_DAY_BASED = '(?P<year>[0-9]{4})(/(?P<month>[0-9]{2})(/(?P<day>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?'
RESOLVE_MONTH_HYPHEN_BASED = '(?P<year>[0-9]{4})(-(?P<month>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+)'
RESOLVE_DAY_HYPHEN_BASED = '(?P<year>[0-9]{4})(-(?P<month>[0-9]{2})(-(?P<day>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?'

RESOLVES = (
    (RESOLVE_NORMAL,_('Normal (slug)')),

    (RESOLVE_YEAR_BASED,_('Year based (YYYY/slug)')),
    (RESOLVE_MONTH_BASED,_('Month based (YYYY/MM/slug)')),
    (RESOLVE_DAY_BASED,_('Day based (YYYY/MM/DD/slug)')),
    
    (RESOLVE_MONTH_HYPHEN_BASED,_('Month based (YYYY-MM/slug)')),
    (RESOLVE_DAY_HYPHEN_BASED,_('Day based (YYYY-MM-DD/slug)')),
)

REDIRECT_TARGET_SAME = ""
REDIRECT_TARGET_BLANK = "_blank"

REDIRECT_TARGETS = (
    (REDIRECT_TARGET_SAME, _("Same window")),
    (REDIRECT_TARGET_BLANK, _("New window")),
)