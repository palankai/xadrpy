'''
Created on 2011.05.05.

@author: pcsaba
'''
from django.db import models
import datetime
from django.contrib.sites.models import Site
from django.db.models import Q
import conf
from django.contrib.auth.models import User

class PermanentSessionManager( models.Manager ):
    use_for_related_fields = True
    
    def get_active_session(self):
        return self.filter(Q(expiry__isnull=True) | Q(expiry__gt=datetime.datetime.now()))
    
    def get_active_users(self):
        return User.objects.filter(pk__in=self.get_active_session())
    
    def renew(self, request):
        permanent_session = self.model( site = Site.objects.get_current(), user = request.user if not request.user.is_anonymous() else None )
        permanent_session.save()
        setattr(request, conf.REQUEST_KEY, permanent_session)
        request.session[conf.SESSION_KEY] = permanent_session.id
        return permanent_session
    
    def get_current(self, request):
        permanent_session_id = request.session.get( conf.SESSION_KEY, None )
        if permanent_session_id:
            try:
                permanent_session = self.model.objects.get( pk = permanent_session_id )
                if request.user.is_anonymous() and permanent_session.user != None:
                    permanent_session.user = None
                    permanent_session.save()
                if not request.user.is_anonymous() and permanent_session.user != request.user:
                    permanent_session.user = request.user
                    permanent_session.save()
                return permanent_session
            except self.model.DoesNotExist:
                pass
        return self.renew( request )
