from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from xadrpy.contrib.feedback.forms import TrackbackForm
from xadrpy.contrib.feedback.models import Feedback

@require_POST
def receive_trackback(request, content_type_id, object_id):
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    site = Site.objects.get_current()
    
    form = TrackbackForm(request.POST)
    if form.is_valid():
        feedback = Feedback()
        feedback.url = form.cleaned_data['url']
        feedback.title = form.cleaned_data['title']
        feedback.site_name = form.cleaned_data['blog_name']
        feedback.comment = form.cleaned_data['excerpt']
        feedback.content_object = obj
        feedback.ip_address = request.META['REMOTE_ADDR']
        feedback.site = site
        feedback.is_remote = True
        feedback.save()
        return render_to_response("feedback/trackback_response.xml", {'error': False}, mimetype="text/xml")
    else:
        context = {'error': True,
                   'message': "\n".join(form.errors)
                  }
        return render_to_response("feedback/trackback_response.xml", context, mimetype="text/xml")

def receive_pingback(request):
    pass
#    from xadrpy.vendor.trackback import views
#    return views.receive_pingback(request)