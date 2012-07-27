'''
Created on 2012.07.27.

@author: pcsaba
'''
from django import forms
from xadrpy.contrib.blog.models import Post, Column
from xadrpy.contrib.pages.forms import PageAdminForm

class ColumnAdminForm(PageAdminForm):
    class Meta:
        model = Column

class PostAdminForm(forms.ModelForm):
    
    class Meta:
        model = Post
