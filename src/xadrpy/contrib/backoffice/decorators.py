from django.http import HttpResponse
from django.conf import settings
from xadrpy.utils.jsonlib import JSONEncoder
import traceback, sys

try:
    import json
except:
    import simplejson as json

def _get_stack():
    if not settings.DEBUG: 
        return []
    stack = []
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for row in traceback.extract_tb(exc_traceback):
        stack.append("%s:%s %s() %s" % (row[0], row[1], row[2],row[3]))
    stack.reverse()
    return stack

class RequestParams(object):
    def __init__(self):
        self.orders = []
        self.filters = {}
        self.groups = []
        self.limit = None
        self.start = 0
        
    

def backoffice_response(func=None, pattern=None, kwargs=None, root="response", successProperty="success", totalProperty="total", directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start"):
    
    def inner(func):

        def view_func_wrapper(request, *args, **kwargs):
            try:
                if request.method == "POST":
                    try:
                        request.DATA = json.loads(request.body)
                    except:
                        request.DATA = {}
                request.PARAMS = RequestParams() 
                if sortParam in request.GET:
                    orders = []
                    for item in json.loads(request.GET.get(sortParam)):
                        if item['direction']=="DESC":
                            orders.append("-"+item["property"])
                        else:
                            orders.append(item["property"])
                    request.PARAMS.orders = orders
                if filterParam in request.GET:
                    filters = {}
                    for item in json.loads(request.GET.get(filterParam)):
                        filters[item['property']]=item['value']
                    request.PARAMS.filters = filters
                if limitParam in request.GET:
                    request.PARAMS.limit = request.GET.get(limitParam)
                if startParam in request.GET:
                    request.PARAMS.start = request.GET.get(startParam)
                if pageParam in request.GET:
                    request.PARAMS.page = request.GET.get(pageParam)
                    
                if root == None:
                    response = JSONEncoder().encode(func(request, *args, **kwargs))
                else:
                    response = {}
                    response['success'] = True
                    response[root] = func(request, *args, **kwargs)
                    if isinstance(response[root], tuple):
                        response[totalProperty] = response[root][1] 
                        response[root] =  response[root][0]
                    response = JSONEncoder().encode(response)
            except Exception, e:
                response = HttpResponse(JSONEncoder().encode({
                                                "success": False, 
                                                "error": {
                                                    "text": len(e.args) and e.args[0] or "", 
                                                    "exception": e.__class__.__name__,
                                                    "args": e.args[1:],
                                                    "kwargs": e.__dict__,
                                                    "stack": _get_stack(),
                                                    "level": "error",
                                                    }
                                                }),
                                         mimetype="application/json")
            if isinstance(response, HttpResponse):
                return response
            return HttpResponse(response, mimetype="application/json")
        
        view_func_wrapper._backoffice_params = {
                    'pattern': pattern or r"%s/$" % func.__name__,
                    'kwargs': kwargs
                }            
        return view_func_wrapper

    if func:
        return inner(func)
    else:
        return inner
