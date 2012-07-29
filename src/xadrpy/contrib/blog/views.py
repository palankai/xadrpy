from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import Http404
import logging
from django.utils.safestring import mark_safe
from xadrpy.contrib.blog.models import Category
logger = logging.getLogger("blog")

def column(request, route, **kwargs):
    ctx = route.get_context(request)
    route.increment_view_count(request)
    return render_to_response(request.theme.template().column, ctx, RequestContext(request))

def categories(request, slug, route=None, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    ctx = {
        'category': category,
        'entries': category.get_entries(),
    }
    return render_to_response("xadrpy/blog/categories.html", ctx, RequestContext(request))

def tag(request, route, **kwargs):
    pass

def posts(request, route, title, **kwargs):        
    posts = route.posts.filter(**kwargs)
    ctx = {
        'column': route,
        'title': title % kwargs,
        'posts': posts,
    }
    return render_to_response("post_list.html", ctx, RequestContext(request))

def entry(request, route, **kwargs):
    entry = route.get_entry(**kwargs)
    entry.permit(request)
    ctx = dict(route.get_context(request),
               **entry.get_context(request))
    entry.increment_view_count(request)
    return render_to_response("xadrpy/blog/entry.html", ctx, RequestContext(request))

    