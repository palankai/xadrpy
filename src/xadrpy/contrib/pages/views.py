from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger("x-pages")

def page(request):
    ctx = request.route.get_context(request)
    request.route.increment_view_count(request)
    return render_to_response(request.theme.template().page, ctx, RequestContext(request))
