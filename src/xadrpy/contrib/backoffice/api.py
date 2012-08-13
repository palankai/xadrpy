from django.contrib import auth
from xadrpy.contrib.backoffice.forms import LoginForm, AddUserForm, EditUserForm,\
    PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from xadrpy.core.forms.exceptions import FormException
from xadrpy.core.api.decorators import APIInterface

api = APIInterface(r"xadrpy.contrib.backoffice/")

@api.response(permissions=False)
def login(request):
    if request.user.is_authenticated():
        auth.logout(request)
    form = LoginForm(request.POST)
    if form.is_valid():
        user = form.get_user()
        auth.login(request, user)
        return
    raise Exception("Invalid username or password")

@api.response
def user_list(request):
    users = User.objects.all()
    return [{
        'id': user.id,
        'username': user.username,
        'full_name': ("%s %s" % (user.last_name,user.first_name)).strip(),
        'display': "%s %s (%s)" % (user.last_name,user.first_name,user.username) if user.first_name and user.last_name else user.username,
    } for user in users]
