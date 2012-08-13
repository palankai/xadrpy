from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext as _
from xadrpy.core.models.fields.nullchar_field import NullCharField
from xadrpy.core.models.fields.list_field import ListField
from xadrpy.core.models.fields.object_field import ObjectField
import conf
import base
from managers import ConsumerManager
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
import datetime

class OwnedModel(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_("User"))
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name=_("Group"))
    
    class Meta:
        abstract = True
#        permissions = (
#            ("view_", "Can see available tasks"),
#        )
        
class Instance(models.Model):
    key = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Instance")
        verbose_name_plural = _("Instance")
        db_table = "xadrpy_access_instance"

class Role(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, verbose_name=_('Permissions'), blank=True, db_table="xadrpy_access_role_permissions")
    groups = models.ManyToManyField(Group, verbose_name=_('Groups'), blank=True, db_table="xadrpy_access_role_groups")
    status = models.IntegerField(default=1, db_index=True)
    scope = ListField(default=[], verbose_name=_("Scope"))

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        db_table = "xadrpy_access_role"
        unique_together = (("site", "key"),("site", "name"),)

class Account(models.Model):
    key = NullCharField(max_length=255, verbose_name=_("Account key"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    user =  models.ForeignKey(User, verbose_name=_("User"), related_name="+")
    status = models.IntegerField(default=1, db_index=True)
    scope = ListField(default=[], verbose_name=_("Scope"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        db_table = "xadrpy_access_account"

@receiver(pre_save, sender=Account)
def account_generate_key(sender, instance, **kwargs):
    if instance.key == None:
        instance.key = base.KeyGenerator(conf.ACCOUNT_KEY_LENGTH)()
    
class Rule(models.Model):
    account = models.ForeignKey(Account, related_name="+")
    user = models.ForeignKey(User, related_name="+")
    roles = models.ManyToManyField(Role, verbose_name=_('Roles'), blank=True, db_table="xadrpy_access_rule_roles")
    scope = ListField(default=[], verbose_name=_("Scope"))

    class Meta:
        verbose_name = _("Rule")
        verbose_name_plural = _("Rule")
        db_table = "xadrpy_access_rule"

class UserScope(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    group = models.ForeignKey(Group, verbose_name=_("Main group"), blank=True, null=True, related_name="+")
    user =  models.ForeignKey(User, verbose_name=_("User"), related_name="+")
    scope = ListField(default=[], verbose_name=_("Scope"))

    class Meta:
        verbose_name = _("User scope")
        verbose_name_plural = _("Users scope")
        db_table = "xadrpy_access_user_scope"
        unique_together = ("site", "user")

class GroupScope(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    group =  models.ForeignKey(Group, verbose_name=_("Group"), related_name="+")
    scope = ListField(default=[], verbose_name=_("Scope"))

    class Meta:
        verbose_name = _("User scope")
        verbose_name_plural = _("Users scope")
        db_table = "xadrpy_access_group_scope"
        unique_together = ("site", "group")

class Consumer(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    static_key = NullCharField(max_length=255, verbose_name=_("Static key"))
    consumer_id = NullCharField(max_length=255, verbose_name=_("Consumer ID"), unique=True)
    consumer_secret = NullCharField(max_length=255, verbose_name=_("Consumer secret"))
    consumer_type = NullCharField(max_length=255, verbose_name=_("Consumer type"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    scope = ListField(default=[], verbose_name=_("Scope"))
    redirect_uri = NullCharField(max_length=255)
    status = models.IntegerField(default=1, db_index=True)
    keys = ObjectField(_("Keys"))
    
    objects = ConsumerManager()
    
    class Meta:
        verbose_name = _("Consumer")
        verbose_name_plural = _("Consumer")
        db_table = "xadrpy_access_consumer"
        unique_together = ("site", "static_key")

    def __unicode__(self):
        return self.name

@receiver(pre_save, sender=Consumer)
def consumer_generate_key   (sender, instance, **kwargs):
    if instance.consumer_id == None:
        instance.consumer_id = base.KeyGenerator(conf.CONSUMER_ID_LENGTH)()
    if instance.consumer_secret == None:
        instance.consumer_secret = base.KeyGenerator(conf.CONSUMER_SECRET_LENGTH)()

class Access(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=255, unique=True, verbose_name=_("Key"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    consumer = models.ForeignKey(Consumer, blank=True, null=True, related_name="+")
    user = models.ForeignKey(User, related_name="+")
    scope = ListField(default=[], verbose_name=_("Scope"))
    status = models.IntegerField(default=1, db_index=True)
    keys = ObjectField(_("Keys"))

    class Meta:
        verbose_name = _("Access")
        verbose_name_plural = _("Access")
        db_table = "xadrpy_access_access"
        unique_together = ("site","consumer","user")

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.consumer)

@receiver(pre_save, sender=Access)
def access_generate_key(sender, instance, **kwargs):
    if instance.key == None:
        instance.key = base.KeyGenerator(conf.ACCOUNT_KEY_LENGTH)

class Token(models.Model):
    token = models.CharField(max_length=255, unique=True, editable=False, verbose_name=_("Token"))
    token_type = NullCharField(max_length=255, verbose_name=_("Token type"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    expired = models.DateTimeField(blank=True, null=True, verbose_name=_("Expired"))
    timeout = models.PositiveIntegerField(default=0, verbose_name=_("timeout"))
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, related_name="+")
    consumer = models.ForeignKey(Consumer, blank=True, null=True, verbose_name=_("Consumer"), related_name="+")
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_("User"), related_name="+")
    invalid = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        db_table = "xadrpy_access_token"

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.user, self.consumer, self.site)
    
    def get_access(self):
        access, created = Access.objects.get_or_create(site=self.site, consumer=self.consumer, user=self.user) #@UnusedVariable
        return access
    
    def is_valid(self):
        if self.invalid: return False
        if self.timeout == 0: return True
        if self.expired == None: return True
        return datetime.datetime.now() >= self.expired

@receiver(pre_save, sender=Token)
def token_expired_pre_save(sender, instance, **kwargs):
    if instance.invalid: return
    if instance.token == None:
        instance.token = base.KeyGenerator(conf.TOKEN_KEY_LENGTH)
    if instance.timeout > 0:
        instance.expired = datetime.datetime.now()+datetime.timedelta(seconds=instance.timeout)
    else:
        instance.expired = None

