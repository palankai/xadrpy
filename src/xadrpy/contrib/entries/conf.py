from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import re

TEMPLATES = getattr(settings, 'PAGES_TEMPLATES', (("page.html", _("Base template")),))
COLUMN_DEFAULT_VIEW = getattr(settings, 'COLUMN_DEFAULT_VIEW', 'xadrpy.contrib.entries.views.column')
#DEFAULT_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_TEMPLATE', 'post.html')

DEFAULT_ENTRY_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_POST_TEMPLATE', 'xadrpy/entries/entry.html')
DEFAULT_ENTRIES_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_POSTS_TEMPLATE', 'xadrpy/entries/entries.html')
DEFAULT_COLUMN_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_COLUMN_TEMPLATE', 'xadrpy/entries/column.html')

POST_STATES = (
    ('DRA', _('Draft')),
    ('PUB', _('Published')),
    ('HID', _('Hidden')),
)

RESOLVE_NORMAL = '(/(?P<slug>[0-9a-zA-Z\-/_]+))?'
RESOLVE_YEAR_BASED = '(/(?P<year>[0-9]{4})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?'
RESOLVE_MONTH_BASED = '(/(?P<year>[0-9]{4})(/(?P<month>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?'
RESOLVE_DAY_BASED = '(/(?P<year>[0-9]{4})(/(?P<month>[0-9]{2})(/(?P<day>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?)?'
RESOLVE_MONTH_HYPHEN_BASED = '(/(?P<year>[0-9]{4})(\-(?P<month>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?'
RESOLVE_DAY_HYPHEN_BASED = '(/(?P<year>[0-9]{4})(\-(?P<month>[0-9]{2})(\-(?P<day>[0-9]{2})(/(?P<slug>[0-9a-zA-Z\-/_]+))?)?)?)?'

RESOLVES = (
    (RESOLVE_NORMAL,_('Normal (slug)')),

    (RESOLVE_YEAR_BASED,_('Year based (YYYY/slug)')),
    (RESOLVE_MONTH_BASED,_('Month based (YYYY/MM/slug)')),
    (RESOLVE_DAY_BASED,_('Day based (YYYY/MM/DD/slug)')),
    
    (RESOLVE_MONTH_HYPHEN_BASED,_('Month based (YYYY-MM/slug)')),
    (RESOLVE_DAY_HYPHEN_BASED,_('Day based (YYYY-MM-DD/slug)')),
)

RESOLVERS = (
    ('xadrpy.contrib.entries.resolvers.MonthBasedResolver',_("Month based resolver")),
    ('xadrpy.contrib.entries.resolvers.BaseResolver',_("Base resolver")),
)
DEFAULT_RESOLVER = "xadrpy.contrib.entries.resolvers.MonthBasedResolver"
RESOLVERS_CACHE = {}

PREFERENCES = (
    {"key":"comments_enabled", "namespace":"x-entries", "value": True},
    {"key":"comments_locked", "namespace":"x-entries", "value": False}
)
if hasattr(settings, "PAGE_BREAK_RE"):
    PAGE_BREAK_RE = settings.PAGE_BREAK_RE
else:
    PAGE_BREAK_RE = re.compile("""<div style="page-break-after: always;">\s+<span style="display: none;">&nbsp;</span></div>""")
