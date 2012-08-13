from django import forms
from models import Route

class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = Route
