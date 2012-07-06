from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from xadrpy.models.fields import JSONField, NullCharField 
from xadrpy.api.managers import ClientManager, AccessManager,\
    TokenManager
import libs
import conf
import datetime
from xadrpy.utils.jsonlib import JSONEncoder
from django.utils import simplejson

class Client(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, verbose_name=_("Client name"))
    static_key = NullCharField(max_length=255, verbose_name=_("Client Static key"), unique=True)
    client_id = NullCharField(max_length=255, verbose_name=_("Client ID"), unique=True)
    client_secret = NullCharField(max_length=255, verbose_name=_("Client secret"))
    client_type = NullCharField(max_length=255, verbose_name=_("Client type"))
    scope = JSONField(default=[], verbose_name=_("Scope"))
    data = JSONField(default={}, verbose_name=_("Application data"))
    redirect_uri = NullCharField(max_length=255)

    objects = ClientManager() 

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Client")
        db_table = "xadrpy_api_client"

    def __unicode__(self):
        return self.name
    
    def generate_keys(self, save=True):
        self.client_id = libs.KeyGenerator(conf.KEY_LENGTH)()
        self.client_secret = libs.KeyGenerator(conf.KEY_LENGTH)()
        if save:
            self.save()

class Access(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    scope = JSONField(default=[], verbose_name=_("Scope"))
    data = JSONField(default={}, verbose_name=_("Data"))

    objects = AccessManager()

    class Meta:
        verbose_name = _("Access")
        verbose_name_plural = _("Accesses")
        db_table = "xadrpy_api_access"
        unique_together = ("user","client")

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.client)

class Token(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField(blank=True, null=True)
    timeout = models.PositiveIntegerField(default=0)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User, blank=True, null=True)
    token = models.CharField(max_length=255, unique=True)
    data = JSONField(default={})
    
    objects = TokenManager()

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        db_table = "xadrpy_api_token"

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.client)

    def generate_token(self, save=True):
        self.token = libs.KeyGenerator(conf.KEY_LENGTH)()
        if save:
            self.save()
    
    def update_expired(self):
        if self.timeout == 0:
            self.expired = None
        else:
            self.expired = libs.ExpiredGenerator(seconds=self.timeout)()
        self.save()
    
    def is_expired(self):
        if self.timeout == 0:
            return False
        return datetime.datetime.now() < self.expired
