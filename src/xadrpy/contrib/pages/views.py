from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger("x-pages")

def page(request, route=None):
    logger.debug(route.content)
    ctx = route.get_context(request)
    logger.debug(route.content)
    route.increment_view_count()
    logger.debug(route.content)
    return render_to_response(request.theme.template().page, ctx, RequestContext(request))
