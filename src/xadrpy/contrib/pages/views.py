'''
Created on 2012.07.09.

@author: pcsaba
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from django.http import Http404

def page(request, route=None):
    if not route.can_render():
        raise Http404()

    if request.method == "POST" and route.enable_comments:
        add_page_comments(request, route)

    return route.render_to_response(request)

def add_page_comments(request, route):
    if not route.can_render():
        raise Http404()
    
    return route.render_to_response(request)

