from xadrpy.core.api.decorators import APIObject
from xadrpy.utils.declarative import BaseField
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.core.urlresolvers import reverse

class Field(BaseField):
    xtype = "textfield"
    
    def __init__(self, **kwargs):
        kwargs.update({'xtype': self.xtype})
        self.kwargs = kwargs
    
    def to_data(self):
        return
    
class TextField(Field):
    xtype = "textfield"

class CheckboxField(Field):
    xtype = "displayfield"

class ComboboxField(Field):
    xtype = "displayfield"

class DateField(Field):
    xtype = "displayfield"

class DisplayField(Field):
    xtype = "displayfield"

class FileField(Field):
    xtype = "filefield"

class HiddenField(Field):
    xtype = "filefield"

class HtmlEditorField(Field):
    xtype = "filefield"

class NumberField(Field):
    xtype = "filefield"

class PickerField(Field):
    xtype = "filefield"

class RadioField(Field):
    xtype = "filefield"

class SpinnerField(Field):
    xtype = "filefield"

class TextAreaField(Field):
    xtype = "filefield"

class TimeField(Field):
    xtype = "filefield"

class DateTimeField(Field):
    xtype = "filefield"

class FormPanelOptions(object):
    def __init__(self, options=None):
        self.name = getattr(options, 'name', None)
        self.template = getattr(options, 'template', "xadrpy/backoffice/generic/formpanel.js")
        self.form = getattr(options, 'form', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        
        self.title = getattr(options, 'title','')
        self.modal = getattr(options, 'modal', True)
        self.iconCls = getattr(options, 'iconCls', None)
        self.monitorValid = getattr(options, 'monitorValid', True)


class BaseFormPanel(APIObject):

    @APIObject.response
    def submit(self, request):
        pass
    
    def render(self, request):
        ctx = {
            'name': self._meta.name,
            'submit': reverse(self.submit),
            'options': self._meta,
            'fields': [field.to_data() for field in self.base_fields.values()], 
        }
        return render_to_string(self._meta.template, ctx, RequestContext(request))

    def register_in_api(self, interface, prefix):
        if not self._meta.name:
            self._meta.name = interface.namespace+".view."+self.__class__.__name__
        super(BaseFormPanel, self).register_in_api(interface, prefix)
    