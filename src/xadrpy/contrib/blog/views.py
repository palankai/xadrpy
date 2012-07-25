from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404
from xadrpy.contrib.pages.views import add_page_comments

def column(request, route, **kwargs):
    if not route.can_render():
        raise Http404()

    if request.method == "POST" and route.enable_comments:
        add_page_comments(request, route)

    return route.render_to_response(request)

def category(request, route, **kwargs):
    pass

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

def post(request, route=None, **kwargs):
    try:
        post = route.posts.filter(**kwargs)[0]
    except:
        raise Http404()
    if not post.can_render():
        raise Http404()
    return post.render_to_response(request)

    