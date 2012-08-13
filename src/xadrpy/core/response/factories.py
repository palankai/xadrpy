from json import JSONResponse, JSONExceptionResponse 
from json import ComplexJSONResponse, ComplexJSONExceptionResponse
from conf import DEFAULT_JSON_RESPONSE

class FactoryCreator(object):
    def __init__(self):
        self.factories = {
            'base': BaseJSONFactory(),
            'complex': ComplexJSONFactory()
        }
        self.set_default_factory(DEFAULT_JSON_RESPONSE)
    
    def get_factory(self, name):
        return self.factories[name]
    
    def add_factory(self, name, factory):
        self.factories[name] = factory
    
    def set_default_factory(self, name):
        self.factories['default'] = self.factories[name]

class BaseJSONFactory(object):
    
    def create_response(self, content):
        return JSONResponse(content)
    
    def create_error_response(self, exception):
        return JSONExceptionResponse(exception)

class ComplexJSONFactory(BaseJSONFactory):
    
    def create_response(self, content):
        return ComplexJSONResponse(content)

    def create_error_response(self, exception):
        return ComplexJSONExceptionResponse(exception)

factory_creator = FactoryCreator()