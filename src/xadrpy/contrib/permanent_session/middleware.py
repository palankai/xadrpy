'''
Created on 2011.05.05.

@author: pcsaba
'''
from models import PermanentSession
import conf
from django.http import HttpResponse
from xadrpy.contrib.permanent_session.exceptions import ReturnResponseFromTriggerException

class PermanentSessionMiddleware( object ):

    def process_request( self, request ):
        self._init(request)
        self._set_permanent_session_on_request()
        try:
            self._run_triggers()
        except ReturnResponseFromTriggerException, e:
            return e.get_response()
    
    def _init(self, request):
        self.permanent_session = PermanentSession.objects.get_current(request)
        self.request = request
    
    def _set_permanent_session_on_request(self):
        setattr(self.request,conf.REQUEST_KEY, self.permanent_session)
    
    def _run_triggers(self):
        for trigger in self._get_triggers():
            self._run_one_trigger(trigger)

    def _get_triggers(self):
        return self.permanent_session.triggers.order_by("priority")
    
    def _run_one_trigger(self, trigger):
        try:
            response = trigger.run(self.request)
        finally:
            if trigger.need_delete(self.request):
                trigger.delete()
        if isinstance(response, HttpResponse):
            raise ReturnResponseFromTriggerException(response)
        
