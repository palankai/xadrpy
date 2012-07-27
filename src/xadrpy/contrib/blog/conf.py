from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import re

TEMPLATES = getattr(settings, 'PAGES_TEMPLATES', (("page.html", _("Base template")),))
DEFAULT_VIEW = getattr(settings, 'BLOG_DEFAULT_VIEW', 'xadrpy.contrib.blog.views.column')
DEFAULT_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_TEMPLATE', 'post.html')

DEFAULT_POST_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_POST_TEMPLATE', 'xadrpy/blog/post.html')
DEFAULT_POSTS_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_POSTS_TEMPLATE', 'xadrpy/blog/posts.html')
DEFAULT_COLUMN_TEMPLATE = getattr(settings, 'BLOG_DEFAULT_COLUMN_TEMPLATE', 'xadrpy/blog/column.html')

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
    ('xadrpy.contrib.blog.resolvers.MonthBasedResolver',_("Month based resolver")),
    ('xadrpy.contrib.blog.resolvers.BaseResolver',_("Base resolver")),
)
DEFAULT_RESOLVER = "xadrpy.contrib.blog.resolvers.MonthBasedResolver"
RESOLVERS_CACHE = {}

PREFERENCES = (
    {"key":"comments_enabled", "namespace":"x-blog", "value": True, "vtype": "bool"},
    {"key":"comments_locked", "namespace":"x-blog", "value": False, "vtype": "bool"}
)
if hasattr(settings, "PAGE_BREAK_RE"):
    PAGE_BREAK_RE = settings.PAGE_BREAK_RE
else:
    PAGE_BREAK_RE = re.compile("""<div style="page-break-after: always;">\s+<span style="display: none;">&nbsp;</span></div>""")
