from django import forms
from xadrpy.contrib.pages.models import Page

class PageAdminForm(forms.ModelForm):

    menu_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    layout_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    skin_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    meta_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    meta_keywords = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    meta_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    overwrite_meta_title = forms.BooleanField(required=False)
    
    extra_classes = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
        
    _meta_fields = ['menu_title', 'skin_name', 'layout_name', 'extra_classes', 'meta_title', 'meta_keywords', 'meta_description', 'overwrite_meta_title']

    class Meta:
        model = Page

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            kwargs['initial']={}
            for k in self._meta_fields:
                kwargs['initial'][k] = kwargs['instance'].meta.get(k,"")
        super(PageAdminForm, self).__init__(*args, **kwargs)

class PageCreateAdminForm(forms.ModelForm):
    class Meta:
        model = Page
    