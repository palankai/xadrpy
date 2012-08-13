import unittest2
from xadrpy.core.response.decorators import encode_response
from django.http import HttpResponse
from xadrpy.core.response.json import JSONResponse

class DecoratorTestCase(unittest2.TestCase):
    
    def test_decorate_view_function(self):

        @encode_response
        def test_view(request):
            pass

        
        resp = test_view(None)
        
        self.assertIsInstance(resp, HttpResponse)
        self.assertIsInstance(resp, JSONResponse)
        self.assertEqual(str(resp),"Content-Type: application/json\n\nnull")
    
    def test_boolean_view_function(self):

        @encode_response
        def test_view(request):
            return True
        
        resp = test_view(None)

        self.assertIsInstance(resp, HttpResponse)
        self.assertIsInstance(resp, JSONResponse)
        self.assertEqual(str(resp),"Content-Type: application/json\n\ntrue")

    
    def test_dict_view_function(self):

        @encode_response
        def test_view(request):
            return {
                'bool': True,
                'int': 12,
                'string': 'Ok'
            }
        
        resp = test_view(None)

        self.assertIsInstance(resp, HttpResponse)
        self.assertIsInstance(resp, JSONResponse)
        self.assertEqual(str(resp),"""Content-Type: application/json\n\n{"int": 12, "bool": true, "string": "Ok"}""")

    def test_complex_view_function(self):

        @encode_response(factory="complex")
        def test_view(request):
            return {
                'bool': True,
                'int': 12,
                'string': 'Ok'
            }
        
        resp = test_view(None)

        self.assertIsInstance(resp, HttpResponse)
        self.assertIsInstance(resp, JSONResponse)
        self.assertEqual(str(resp),"""Content-Type: application/json\n\n{"notifications": [], "result": {"int": 12, "bool": true, "string": "Ok"}, "success": true, "triggers": []}""")
    
    def test_HttpResonse_view_function(self):

        @encode_response
        def test_view(request):
            return HttpResponse("Ok")
        
        resp = test_view(None)

        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(str(resp),"Content-Type: text/html; charset=utf-8\n\nOk")
        
    def test_exception_view_function(self):
        
        @encode_response
        def test_view(request):
            raise Exception("Hiba")

        resp = test_view(None)

        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(str(resp),"""X-Exception: Exception\nContent-Type: application/json\n\n{"stack": [], "message": "Hiba", "args": [], "class": "Exception", "kwargs": {}}""")
