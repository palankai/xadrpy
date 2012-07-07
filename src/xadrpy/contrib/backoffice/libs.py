from django.utils.datastructures import SortedDict
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from copy import deepcopy
from django.forms.models import ModelForm
from django.forms.fields import CharField

class BaseField(object):
    creation_counter = 0
    
    def __init__(self, name, source_field):
        self.name = name
        self.source_field = source_field

class TestField(object):

    creation_counter = 0
    
    def __init__(self, field=None, kwargs=[]):
        self.field = field
        self.kwargs = kwargs

class ModelBasedOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.widgets = getattr(options, 'widgets', None)

class BaseSome(object):
    def __init__(self):
        opts = self._meta
        self.fields = deepcopy(self.base_fields)

class Some(BaseSome):
    __metaclass__ = get_metaclass(BaseSome, ModelBasedOptions, TestField, "model")

class DSome(Some):
    test = TestField()
    class Meta:
        model = User

class UForm(ModelForm):
    test2 = CharField()
    class Meta:
        model = User

class FormBasedOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.form = getattr(options, 'form', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.widgets = getattr(options, 'widgets', None)

class Some2(BaseSome):
    __metaclass__ = get_metaclass(BaseSome, FormBasedOptions, TestField, "form")

class DSome2(Some2):
    test = TestField()
    class Meta:
        model = User
        form = UForm
