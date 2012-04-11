
class ReturnResponseFromTriggerException(Exception):
    def __init__(self, response, *args, **kwargs):
        self._response = response
        Exception.__init__(self, *args, **kwargs)
    
    def get_response(self):
        return self._response