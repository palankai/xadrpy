from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.safestring import mark_safe

def page(request, route=None):
    ctx = route.get_context(request)
    route.increment_view_count()
    return render_to_response(request.theme.template().page, ctx, RequestContext(request))
