from xadrpy.utils.inspector import is_method
from django.http import HttpResponse
from factories import factory_creator

def encode_response(func=None, factory="default"):
    factory_object = factory_creator.get_factory(factory)
    
    def inner(func):

        def view_func_wrapper(request, *args, **kwargs):
            try:
                response = func(request, *args, **kwargs)
            except Exception, e:
                response = factory_object.create_error_response(e)

            if isinstance(response, HttpResponse):
                return response
            
            return factory_object.create_response(response)

        return view_func_wrapper
    
    if func:
        return inner(func)
    else:
        return inner
