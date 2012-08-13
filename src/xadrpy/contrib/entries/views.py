from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import logging
from models import Category
from xadrpy.utils.paginator import Paginated
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import Http404
logger = logging.getLogger("xadrpy.contrib.entries.views")

def column(request):
    entries = request.route.get_entries()
    paginated = Paginated(entries, 5, orphans=1, page_url=u"?"+_("page")+"=%(index)s")
    paginated.set_first_page(reverse("xadrpy.contrib.entries.views.column", kwargs={"route_id": request.route.id}))
    paginated.set_page(request.GET.get(_("page"),1))
    ctx = {
        'content': request.route.get_content(),
        'content_title': request.route.get_title(),
        'show_content': request.route.show_content,
        'entries': paginated,
    }
    request.route.increment_view_count(request)
    return render_to_response("xadrpy/entries/column.html", ctx, RequestContext(request))

def categories(request, slug=None, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    ctx = {
        'category': category,
        'entries': category.get_entries(),
    }
    return render_to_response("xadrpy/entries/categories.html", ctx, RequestContext(request))

def tag(request, route, **kwargs):
    pass

def posts(request, title, **kwargs):        
    posts = request.route.posts.filter(**kwargs)
    ctx = {
        'column': request.route,
        'title': title % kwargs,
        'posts': posts,
    }
    return render_to_response("post_list.html", ctx, RequestContext(request))

def entry(request, **kwargs):
    entry = request.route.get_entry(**kwargs)
    if not entry.can_render():
        raise Http404()
    ctx = {
        'entry': entry
    }
    entry.increment_view_count(request)
    return render_to_response("xadrpy/entries/entry.html", ctx, RequestContext(request))

