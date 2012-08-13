# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from managers import PermanentSessionManager
from django.contrib.sites.models import Site
from xadrpy.core.models.fields import ObjectField
import datetime
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from xadrpy.core.models.inheritable import Inheritable

class PermanentSession(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"))
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_("User"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    expiry_age = models.IntegerField(_("Expiry age"), blank=True, null=True)
    expiry = models.DateTimeField(_("Expiry"), blank=True, null=True)
    data = ObjectField(_("Data"))

    objects = PermanentSessionManager()
    
    class Meta:
        verbose_name = _("Permanent session")
        verbose_name_plural = _("Permanent sessions")
        db_table = "xadrpy_permanent_session"

    def __unicode__(self):
        if self.user:
            return _("Permanent session (%(name)s)") % self.user
        return _(u"Permanent session (guest)")

class Trigger(Inheritable):
    permanent_session = models.ForeignKey(PermanentSession, related_name="triggers", verbose_name=_("Permanent session"))
    priority = models.IntegerField(default=1)
    
    class Meta:
        db_table = "xadrpy_permanent_session_trigger"
        
    
    def run(self, request):
        pass
    
    def need_delete(self, request):
        return True

@receiver(pre_save, sender=PermanentSession)
def permanent_session_expiry_pre_save(sender, instance, **kwargs):
    if instance.expiry_age:
        instance.expiry = datetime.datetime.now()+datetime.timedelta(seconds=instance.expiry_age)
    else:
        instance.expiry_age = None
        instance.expiry = None
    