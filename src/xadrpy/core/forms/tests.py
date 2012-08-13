import unittest2
from django import forms
from exceptions import FormException
from xadrpy.core.response.decorators import encode_response
from xadrpy.core.response.json import JSONExceptionResponse

class TestForm(forms.Form):
    name = forms.CharField()

class FormExceptionTestCase(unittest2.TestCase):
    
    def test_single_form_exception(self):
        test_form = TestForm()
        self.assertFalse(test_form.is_valid())

        @encode_response
        def view(request):
            test_form = TestForm({})
            test_form.is_valid()
            raise FormException(test_form)
        
        response = view(None)
        self.assertIsInstance(response, JSONExceptionResponse)
        self.assertEqual(str(response), """X-Exception: FormException\nContent-Type: application/json\n\n{"stack": [], "message": "", "args": [], "class": "FormException", "kwargs": {"fields": {"name": "Name"}, "field_errors": {"name": ["This field is required."]}, "non_field_errors": []}}""") 
    
        
