from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404

def posts(request, route, title, **kwargs):        
    posts = route.posts.filter(**kwargs)
    ctx = {
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

    