'''
Created on 2012.07.27.

@author: pcsaba
'''
from django import forms
from models import Entry, Column
from xadrpy.contrib.pages.forms import PageAdminForm

class ColumnAdminForm(PageAdminForm):
    class Meta:
        model = Column

class EntryAdminForm(forms.ModelForm):
    
    class Meta:
        model = Entry
