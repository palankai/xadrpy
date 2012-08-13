from django.http import HttpResponse
from xadrpy.utils.jsonlib import JSONEncoder
import traceback, sys
from conf import EXCEPTION_RESPONSE_NEED_STACK, JSON_MIMETYPE

class JSONResponse(HttpResponse):

    def __init__(self, content=None, status=200):
        super(JSONResponse, self).__init__(content=None, status=status, mimetype=JSON_MIMETYPE)
        self._json_cache = content

    def _format_content(self, content):
        return content
    
    def _encode(self, value):
        return JSONEncoder().encode(value)

    def _get_content(self):
        return self._encode(self._format_content(self._json_cache))

    def _set_content(self, value):
        self._json_cache=value

    content = property(_get_content, _set_content)
    
    def __iter__(self):
        self._container = [self._get_content()]
        return super(JSONResponse, self).__iter__()


class JSONExceptionResponse(JSONResponse):
    
    def __init__(self, exception, status=400):
        self.exception = exception
        content = self.get_exception_content()

        super(JSONExceptionResponse, self).__init__(content=content,status=status)
        self['X-Exception']=exception.__class__.__name__
    
    def get_exception_content(self):
        content = {
            "class": self.exception.__class__.__name__,
            "message": len(self.exception.args) and self.exception.args[0] or "",
            "args": self.exception.args[1:],
            "kwargs": self.exception.__dict__,
            "stack": self.get_stack(),
        }
        return content
    
    def get_stack(self):
        if not EXCEPTION_RESPONSE_NEED_STACK: 
            return []
        stack = []
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for row in traceback.extract_tb(exc_traceback):
            stack.append("%s:%s %s() %s" % (row[0], row[1], row[2],row[3]))
        stack.reverse()
        return stack

class ComplexJSONResponse(JSONResponse):
    
    def __init__(self, content=None):
        JSONResponse.__init__(self, content=content)
        self.notifications = []
        self.triggers = []

    def _format_content(self, content):
        return {
            "success": True,
            "result": content,
            "notifications": self.notifications,
            "triggers": self.triggers,
        }
    
    def add_trigger(self, trigger):
        self.triggers.append(trigger)
    
    def add_notification(self, notification, level='info'):
        self.notifications.append((notification, level))

class ComplexJSONExceptionResponse(JSONExceptionResponse):

    def __init__(self, exception):
        JSONExceptionResponse.__init__(self, exception, status=200)
    
    def get_exception_content(self):
        content = JSONExceptionResponse.get_exception_content(self)
        content["success"] = False
        return content
