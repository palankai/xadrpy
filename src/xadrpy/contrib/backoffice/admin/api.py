from django.contrib import auth
from xadrpy.contrib.backoffice.forms import LoginForm, AddUserForm, EditUserForm,\
    PasswordResetForm, PasswordChangeForm, GroupForm
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from xadrpy.core.forms.exceptions import FormException
from xadrpy.core.api.decorators import APIInterface

api = APIInterface(r"xadrpy.contrib.backoffice.admin/")


@api.response
def get_users(request):
    users = User.objects.all()
    return [{
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': ("%s %s" % (user.last_name,user.first_name)).strip(),
        'display': "%s %s (%s)" % (user.last_name,user.first_name,user.username) if user.first_name and user.last_name else user.username,
        'email': user.email,
        'is_superuser': user.is_superuser
    } for user in users]

@api.response
def get_groups(request):
    groups = Group.objects.all()
    return [{
             'id': group.id,
             'name': group.name
             } for group in groups]

@api.response
def add_group(request):
    form = GroupForm(request.POST)
    if not form.is_valid():
        raise FormException(form)
    form.save()

@api.response(pattern=r"edit_group/(?P<group_id>[0-9]+)/$")
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    form = GroupForm(request.POST, instance=group)
    if not form.is_valid():
        raise FormException(form)
    form.save()

@api.response(pattern=r"del_group/(?P<group_id>[0-9]+)/$")
def del_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()


@api.response
def add_user(request):
    form = AddUserForm(request.POST)
    if form.is_valid():
        user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data['password'])
        user.is_superuser = form.cleaned_data['is_superuser']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
    else:
        raise FormException(form)
    

@api.response(pattern=r"del_user/(?P<user_id>[0-9]+)/$")
def del_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return True

@api.response(pattern=r"edit_user/(?P<user_id>[0-9]+)/$")
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = EditUserForm(request.POST)
    if form.is_valid():
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.is_superuser = form.cleaned_data['is_superuser']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
    else:
        raise FormException(form)

@api.response(pattern=r"reset_password/(?P<user_id>[0-9]+)/$")
def reset_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = PasswordResetForm(request.POST)
    if form.is_valid():
        user.set_password(form.cleaned_data['password'])
        user.save()
    else:
        raise FormException(form)


