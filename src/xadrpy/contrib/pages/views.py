'''
Created on 2012.07.09.

@author: pcsaba
'''
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def root(request, slug=None, year=None, month=None, day=None, route=None):
    page = route.pages.filter(slug=slug or u"")
    print route.resolve
    if not len(page):
        raise Http404(unicode(_("Page not found")))
    page = page[0]
    template = page.layout and page.layout.template or route.layout and route.layout.template or "page.html"
    print year, month, day
    ctx = {
        'route': route,
        'page': page
    }
    return render_to_response(template, ctx, RequestContext(request))
