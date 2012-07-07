from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from xadrpy.auth.base import rights

from xadrpy.api.decorators import APIInterface

api = APIInterface(r"api/")


def home(request):
    pass

def token(request):
    if not request.user.is_authenticate():
        return HttpResponseRedirect(reverse("xadrpy.contrib.api.views.authenticate"))

def authorize(request):
    pass

def authenticate(request):
    pass

@api.response(pattern=False, permissions=False)
def get_permissions(request):
    return rights.get_rights_dict()
