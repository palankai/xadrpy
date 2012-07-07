from django import forms
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
forms.ModelForm

class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super( LoginForm, self).__init__( *args, **kwargs )
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            self.user_cache = authenticate( username=username, password=password )
            if not self.user_cache:
                raise forms.ValidationError(_("Wrong username or password"))
            if not self.user_cache.is_active:
                raise forms.ValidationError(_("Your account is inactive"))

        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache

class AddUserForm(forms.Form):
    username = forms.CharField(min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=3)
    email = forms.EmailField(required=False)
    is_superuser = forms.BooleanField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def clean(self):
        data = super(AddUserForm, self).clean()
        if data['password'] != data['password2']:
            raise forms.ValidationError("These new passwords didn't match!")
        return data

class EditUserForm(forms.Form):
    username = forms.CharField(min_length=3)
    email = forms.EmailField(required=False)
    is_superuser = forms.BooleanField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
    
class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=3)

    def clean(self):
        data = super(PasswordResetForm, self).clean()
        if data['password'] != data['password2']:
            raise forms.ValidationError("These new passwords didn't match!")
        return data

    
class PasswordChangeForm(forms.Form):
    original_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=3)

    def set_user(self, user):
        self._user = user
        
    def clean_original_password(self):
        data = self.cleaned_data['original_password']
        if not self._user.check_password(data):
            raise forms.ValidationError("Original password didn't match")
        return data

    def clean(self):
        data = super(PasswordChangeForm, self).clean()
        if data['password'] != data['password2']:
            raise forms.ValidationError("These new passwords didn't match!")
        return data
    
class GroupForm(forms.ModelForm):
    dt = forms.DateTimeField()
    class Meta:
        model = Group
        fields = ("name",)
