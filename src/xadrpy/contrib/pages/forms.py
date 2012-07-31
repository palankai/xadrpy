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
from filebrowser.fields import FileBrowseFormField, FileBrowseWidget,\
    FileBrowseField
from filebrowser.sites import site

class PageAdminForm(forms.ModelForm):

    menu_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    layout_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    skin_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    extra_classes = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
        
    _meta_fields = ['menu_title', 'skin_name', 'layout_name', 'extra_classes']

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
    