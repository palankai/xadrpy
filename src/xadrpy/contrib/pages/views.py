from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging
logger = logging.getLogger("x-pages")

def page(request):
    ctx = get_page_context(request.route)
    request.route.increment_view_count(request)
    return render_to_response(request.theme.template().page, ctx, RequestContext(request))

def get_page_context(page):
    ctx ={
        'content': page.get_content(),
        'content_title': page.get_title(),
        'show_content': page.show_content,
    }
    return ctx
