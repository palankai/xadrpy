from django.http import HttpResponse, QueryDict
from django.conf import settings
from xadrpy.utils.jsonlib import JSONEncoder
import traceback, sys
import conf
from xadrpy.core.access.exceptions import AuthenticationError

try:
    import json #@UnusedImport
except:
    import simplejson as json #@Reimport

def _get_stack():
    if not settings.DEBUG: 
        return []
    stack = []
    unused, unused, exc_traceback = sys.exc_info()
    for row in traceback.extract_tb(exc_traceback):
        stack.append("%s:%s %s() %s" % (row[0], row[1], row[2],row[3]))
    stack.reverse()
    return stack

def replacer(s):
    if isinstance(s, str) or isinstance(s, unicode):
        for c in ";/?:@&=+$,": 
            s=s.replace(c,"%%%02X" % ord(c))
    return s


class RequestParams(object):
    def __init__(self):
        self.orders = []
        self.filters = {}
        self.groups = []
        self.limit = None
        self.start = 0

class APIInterface(object):
    
    def __init__(self, prefix):
        self.prefix = prefix
    
    def response(self, func=None, pattern=None, kwargs=None, root="response", successProperty="success", totalProperty="total", directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start", permissions=[]):
        def inner(func):
    
            def view_func_wrapper(request, *args, **kwargs):
                try:
                    if permissions != False:
                        self._check_authentication(request)
                        self._check_authorization(request, permissions)
                    self._parse_body(request)
                    self._parse_params(request, directionParam, filterParam, groupParam, limitParam, pageParam, sortParam, startParam)
                    response = self._call_func(func, request, args, kwargs, root, successProperty, totalProperty)
                except Exception, e:
                    response = self._handle_exception(e)
                    
                if isinstance(response, HttpResponse):
                    return response
                
                return HttpResponse(response, mimetype="application/json")
            
            if pattern != False:
                self._append(self.prefix+(pattern or r"%s/$" % func.__name__), view_func_wrapper, kwargs)
            view_func_wrapper.csrf_exempt = True
            return view_func_wrapper
    
        if func:
            return inner(func)
        else:
            return inner

    def _append(self, pattern, method, kwargs):
        conf.urls.append((pattern, method, kwargs))
        
    def _check_authentication(self, request):
        if not request.user.is_authenticated():
            raise AuthenticationError()
    
    def _check_authorization(self, request, permissions):
        pass

    def _parse_body(self, request):
        request.POSTS=[]
        request.DATA = False
        if request.method in ["POST","PUT","DELETE"] :
            try:
                request.DATA = self._decode(request.body)
            except:
                pass
            if isinstance(request.DATA, list):
                for row in request.DATA:
                    for field_name in row:
                        if row[field_name] == None:
                            row[field_name]=""
                    buff=[]
                    for key, value in row.items():
                        print key, value, replacer(value)
                        buff.append(u"%s=%s" % (key, replacer(value)))
                    print buff
                    request.POSTS.append(QueryDict(u"&".join(buff)))
                print request.POSTS
    
    def _parse_params(self, request, directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start"):
        request.PARAMS = RequestParams() 
        if sortParam in request.GET:
            orders = []
            for item in json.loads(request.GET.get(sortParam)):
                if item['direction']=="DESC":
                    orders._append("-"+item["property"])
                else:
                    orders._append(item["property"])
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
    
    def _call_func(self, func, request, args, kwargs, root="response", successProperty="success", totalProperty="total", this=None):
        result = self._call(func, request, args, kwargs, this)
        if isinstance(result, HttpResponse):
            return result
        if root == None:
            response = self._encode(result)
        else:
            response = {}
            response[successProperty] = True
            response[root] = result
            if isinstance(response[root], tuple):
                response[totalProperty] = response[root][1] 
                response[root] =  response[root][0]
            response = self._encode(response)
        return response
    
    def _call(self, func, request, args, kwargs, this=None):
        if this:
            return func(this, request, *args, **kwargs)
        return func(request, *args, **kwargs)
    
    def _handle_exception(self, e):
        return HttpResponse(self._encode({
                "success": False, 
                "error": {
                    "text": len(e.args) and e.args[0] or "", 
                    "exception": e.__class__.__name__,
                    "code": getattr(e, "code", 0),
                    "name": getattr(e, "name", e.__class__.__name__),
                    "args": e.args[1:],
                    "kwargs": e.__dict__,
                    "stack": _get_stack(),
                    "level": "error",
                    }
                }),
         mimetype="application/json", status=200)
    
    def _encode(self, data):
        return JSONEncoder().encode(data)
    
    def _decode(self, string):
        return json.loads(string)

    def register_object(self, obj, pattern=None):
        obj.register_in_api(self, pattern)
    
    def register_class(self, cls, pattern=None):
        cls.register_in_api(self, pattern)

class APIObject(object):
    _interface = None

    @classmethod
    def response(cls, func=None, pattern=None, kwargs=None, root="response", successProperty="success", totalProperty="total", directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start", permissions=[]):
        def inner(func):
            def view_func_wrapper(this, request, *args, **kwargs):
                try:
                    if permissions != False:
                        this._interface._check_authentication(request)
                        this._interface._check_authorization(request, permissions)
                    this._interface._parse_body(request)
                    this._interface._parse_params(request, directionParam, filterParam, groupParam, limitParam, pageParam, sortParam, startParam)
                    response = this._interface._call_func(func, request, args, kwargs, root, successProperty, totalProperty, this=this)
                except Exception, e:
                    response = this._interface._handle_exception(e)
                    
                if isinstance(response, HttpResponse):
                    return response
                
                return HttpResponse(response, mimetype="application/json")

            if pattern != False:
                if pattern == None:
                    view_func_wrapper._APIResponse = (func.__name__, kwargs)
                if type(pattern) == str:
                    view_func_wrapper._APIResponse = (pattern, kwargs)
            view_func_wrapper.csrf_exempt = True
            return view_func_wrapper
        
        if func:
            return inner(func)
        else:
            return inner
    
    def register_in_api(self, interface, prefix):
        prefix = prefix or r"%s/" % self.__class__.__name__
        self._interface = interface
        for member_name in dir(self):
            member = getattr(self, member_name) 
            pattern, kwargs = getattr(member, "_APIResponse", (None,None))
            if pattern:
                interface._append(interface.prefix+prefix+pattern, member, kwargs)

class APIClass(object):

    def __init__(self, _interface):
        self._interface = _interface

    def set_params(self, kwargs):
        return kwargs

    @classmethod
    def response(cls, func=None, pattern=None, kwargs=None, root="response", successProperty="success", totalProperty="total", directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start", permissions=[]):
        def inner(func):
            def view_func_wrapper(this, request, *args, **kwargs):
                try:
                    if permissions != False:
                        this._interface._check_authentication(request)
                        this._interface._check_authorization(request, permissions)
                    this._interface._parse_body(request)
                    this._interface._parse_params(request, directionParam, filterParam, groupParam, limitParam, pageParam, sortParam, startParam)
                    response = this._interface._call_func(func, request, args, kwargs, root, successProperty, totalProperty, this=this)
                except Exception, e:
                    response = this._interface._handle_exception(e)
                    
                if isinstance(response, HttpResponse):
                    return response
                
                return HttpResponse(response, mimetype="application/json")

            if pattern != False:
                if pattern == None:
                    view_func_wrapper._APIResponse = (func, func.__name__, kwargs)
                if type(pattern) == str:
                    view_func_wrapper._APIResponse = (func, pattern, kwargs)
            view_func_wrapper.csrf_exempt = True
            return view_func_wrapper
        
        if func:
            return inner(func)
        else:
            return inner
    
    @classmethod
    def register_in_api(cls, interface, prefix):
        prefix = prefix or r"%s/" % cls.__name__
        for member_name in dir(cls):
            member = getattr(cls, member_name) 
            func, pattern, _kwargs = getattr(member, "_APIResponse", (None,None,None))
            if func and pattern:
                def caller(cls, interface, member):
                    def inner(request, *args, **kwargs):
                        instance = cls(interface)
                        kwargs = instance.set_params(kwargs)
                        return member(instance, request, *args, **kwargs)
                    return inner
                print member_name, member, pattern
                interface._append(interface.prefix+prefix+pattern, caller(cls, interface, member), _kwargs)
    
