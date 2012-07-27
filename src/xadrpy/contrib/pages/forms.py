from django import forms
from xadrpy.contrib.pages.models import Page
from django.db.models.fields.files import ImageField, FileDescriptor,\
    ImageFieldFile
from django.forms.widgets import ClearableFileInput
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.core.files.images import ImageFile
from django.forms.fields import FilePathField

class PageAdminForm(forms.ModelForm):
    meta_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    meta_keywords = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    menu_description = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))
    overwrite_meta_title = forms.BooleanField(required=False)

    menu_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    layout_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    skin_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    extra_classes = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
        
    _meta_fields = ['menu_title', 'skin_name', 'layout_name', 'meta_title', 'meta_keywords','meta_description', 'overwrite_meta_title', 'extra_classes']

    class Meta:
        model = Page

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            kwargs['initial']={}
            for k in self._meta_fields:
                kwargs['initial'][k] = kwargs['instance'].meta.get(k,"")
        super(PageAdminForm, self).__init__(*args, **kwargs)
            