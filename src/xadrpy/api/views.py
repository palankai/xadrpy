from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from xadrpy.auth.base import permissions

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
    permission_list = permissions.get_permissions()
    return [{"name": name, "description": description} for name, description in permission_list] 
