from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from xadrpy.models.fields.nullchar_field import NullCharField
from xadrpy.models.fields.list_field import ListField
from xadrpy.models.fields.object_field import ObjectField
import conf
import libs
from managers import PropertyManager, ConsumerManager
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save, class_prepared
import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from xadrpy.utils.signals import application_started

class UserProxy(User):
    class Meta:
        proxy = True

class GroupProxy(Group):
    class Meta:
        proxy = True
        

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
        instance.key = libs.KeyGenerator(conf.ACCOUNT_KEY_LENGTH)()
    
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
    
    def set_initial_data(self, value):
        Property.objects.get_by(site=self.site, consumer=self).set_value(value)

@receiver(pre_save, sender=Consumer)
def consumer_generate_key   (sender, instance, **kwargs):
    if instance.consumer_id == None:
        instance.consumer_id = libs.KeyGenerator(conf.CONSUMER_ID_LENGTH)()
    if instance.consumer_secret == None:
        instance.consumer_secret = libs.KeyGenerator(conf.CONSUMER_SECRET_LENGTH)()

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
        instance.key = libs.KeyGenerator(conf.ACCOUNT_KEY_LENGTH)

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
        instance.token = libs.KeyGenerator(conf.TOKEN_KEY_LENGTH)
    if instance.timeout > 0:
        instance.expired = datetime.datetime.now()+datetime.timedelta(seconds=instance.timeout)
    else:
        instance.expired = None


class Property(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified"))
    expired = models.DateTimeField(blank=True, null=True)
    timeout = models.PositiveIntegerField(default=0)
    instance = models.ForeignKey(Site, verbose_name=_("Instance"), blank=True, null=True, editable=False, related_name="+")
    site = models.ForeignKey(Site, verbose_name=_("Site"), blank=True, null=True, editable=False, related_name="+")
    consumer = models.ForeignKey(Consumer, verbose_name=_("Consumer"), blank=True, null=True, editable=False, related_name="+")
    account = models.ForeignKey(Account, verbose_name=_("Account"), blank=True, null=True, editable=False, related_name="+")
    rule = models.ForeignKey(Rule, verbose_name=_("Rule"), blank=True, null=True, editable=False, related_name="+")
    role = models.ForeignKey(Role, verbose_name=_("Role"), blank=True, null=True, editable=False, related_name="+")
    group = models.ForeignKey(Group, verbose_name=_("Group"), blank=True, null=True, editable=False, related_name="+")
    user = models.ForeignKey(User, verbose_name=_("User"), blank=True, null=True, editable=False, related_name="+")
    access = models.ForeignKey(Access, verbose_name=_("Access"), blank=True, null=True, editable=False, related_name="+")
    token = models.ForeignKey(Token, verbose_name=_("Token"), blank=True, null=True, editable=False, related_name="+")
    custom_ct = models.ForeignKey(ContentType, verbose_name=_("Custom content type"), blank=True, null=True, editable=False, related_name="+")
    custom_id = models.IntegerField(verbose_name=_("Custom id"), blank=True, null=True, editable=False)
    custom = GenericForeignKey(ct_field="custom_ct", fk_field="custom_id")
    namespace = NullCharField(max_length=255, db_index=True, verbose_name=_("Namespace"), editable=False)
    key = NullCharField(max_length=255, db_index=True, verbose_name=_("Key"), editable=False)
    vtype = NullCharField(max_length=255, verbose_name=_("Format"))
    language_code = NullCharField(max_length=5, db_index=True, verbose_name=_("Language code"), editable=False)
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    description = NullCharField(max_length=255, verbose_name=_("Description"))
    meta = ObjectField(_("Meta data"))
    value = ObjectField(_("Value"))
    invalid = models.BooleanField(default=False, verbose_name=_("Invalid"))
    status = models.IntegerField(default=1)
    source = NullCharField(max_length=255, verbose_name=_("Source"))
    
    objects = PropertyManager(consumer_cls=Consumer, instance_cls=Instance, role_cls=Role)
    
    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        db_table = "xadrpy_access_property"
        unique_together = ("instance","site","account","rule","consumer","role","group","user","access","token", "custom_ct", "custom_id", "namespace", "key", "language_code")

    def __unicode__(self):
        return self.title or "%s# %s" % (self.id, self.key)

    def is_valid(self):
        if self.invalid: return False
        if self.timeout == 0: return True
        if self.expired == None: return True
        return datetime.datetime.now() >= self.expired
    
    def set_value(self, value, language_code=None):
        if not language_code:
            self.value = value
            self.source = None
            self.save()
        if language_code:
            if self.source:
                self.source = None
                self.save()
            alternative = self.get_alternative(language_code)
            alternative.value = value
            alternative.save() 
        
    def get_value(self, language_code=None):
        if not language_code:
            return self.value
        if language_code == True:
            language_code = get_language()
        try:
            alternative = self.alternatives.get(language_code=language_code)
            return alternative.value
        except PropertyAlternative.DoesNotExist:
            return self.value
        
    
    def set_initial_value(self, value, title=None, description=None, meta=None, status=1, vtype=None, source=None):
        self.value = value
        self.title = title
        self.description = description
        self.meta = meta
        self.status = status
        self.vtype = vtype
        self.source = source
        self.save()
    
    def set_initial_alternative(self, language_code, value, title=None, description=None, meta=None, rewrite=False):
        alternative, created = self.get_or_create_alternative(language_code)
        if created or rewrite:
            alternative.title = title
            alternative.description = description
            alternative.meta = meta
            alternative.value = value
            alternative.save()

    def get_alternative(self, language_code):
        alternative, unused = self.get_or_create_alternative(language_code)
        return alternative

    def get_or_create_alternative(self, language_code):
        return PropertyAlternative.objects.get_or_create(base=self, language_code=language_code)
    

class PropertyAlternative(models.Model):
    base = models.ForeignKey(Property, related_name="alternatives")
    language_code = models.CharField(max_length=5, verbose_name=_("Language code"), editable=False)
    title = NullCharField(max_length=255, verbose_name=_("Title"))
    description = NullCharField(max_length=255, verbose_name=_("Description"))
    meta = ObjectField(_("Meta data"))
    value = ObjectField(_("Value"))
    
    class Meta:
        verbose_name = _("Property alternative")
        verbose_name_plural = _("Property alternatives")
        db_table = "xadrpy_access_property_alternative"
        unique_together = ("base","language_code")

def prefs(key=None, default=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, trans=None, order=[]):
    kwargs = {
        'key':key, 
        'instance':instance, 
        'site':site, 
        'consumer':consumer, 
        'account':account, 
        'rule':rule, 
        'role':role, 
        'group':group, 
        'user':user, 
        'access':access, 
        'token':token, 
        'custom':custom, 
        'namespace':namespace, 
        'language_code':language_code,
    }
    pref=Property.objects.get_by(**kwargs)
    while not pref and len(order):
        kwargs.pop(order.pop())
        pref=Property.objects.get_by(**kwargs)
    return pref and pref.get_value(language_code=trans) or default

def prefs_find(**kwargs):
    return Property.objects.find_by(**kwargs)

def prefs_get(value, key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, trans=None):
    return Property.objects.get_by(key=key, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom=custom, namespace=namespace, language_code=language_code)

def prefs_set(value, key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, trans=None):
    pref, unused = Property.objects.get_or_create_by(key=key, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom=custom, namespace=namespace, language_code=language_code)
    pref.value = value
    pref.save()

def prefs_drop(key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None, trans=None):
    try:
        pref = Property.objects.get_by(key=key, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom=custom, namespace=namespace, language_code=language_code)
        pref.delete()
    except Property.DoesNotExist:
        pass

@receiver(pre_save, sender=Property)
def property_expired_pre_save(sender, instance, **kwargs):
    if instance.invalid: return
    if instance.timeout > 0:
        instance.expired = datetime.datetime.now()+datetime.timedelta(seconds=instance.timeout)
    else:
        instance.expired = None

@receiver(application_started)
def property_prepared(**kwargs):
    """
    Read preferences from module's conf and from settings
    """
    
    import imp
    from django.conf import settings
    from django.utils import importlib
    
    def hash_for_dict(d):
        """
        Generate an easy hash for a simple dict
        :param d: a dict
        """
        return ";".join(["%s:%s" % (k,v) for k,v in d.items()])
    
    def process_preference(preferences, preference, source):
        """
        Process a preference
        
        :param preferences: common preferences dict
        :param preference: simple dict
        """
        instance=preference.get("instance",None) 
        site=preference.get("site",None) 
        consumer=preference.get("consumer",None)
        role=preference.get("role",None) 
        namespace=preference.get("namespace",None)
        key=preference.get("key",None)
        language_code=preference.get("language_code",None)
        
        value=preference.get("value", None) 
        vtype=preference.get("vtype", None) 
        title=preference.get("title", None)
        description=preference.get("description", None)
        meta=preference.get("meta", None)
        status=preference.get("status", 1)
        init=preference.get("init", False)
        debug=preference.get("debug", False)
        trans=preference.get("trans", {})
        
        k = {'instance': instance, 'site': site, 'consumer': consumer, 'role': role, 'namespace': namespace, 'key': key, 'language_code': language_code}
        v = {'value': value, 'vtype': vtype, 'title': title, 'description': description, 'meta': meta, 'status': status, 'init': init, 'debug': debug, 'trans': trans, 'source': source}
        v.update(k)
        h = hash_for_dict(k)
        
        if h in preferences:
            preferences[h].update(v)
        else:
            preferences[h]=v

    preferences = dict()

    for app in settings.INSTALLED_APPS:

        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('conf', app_path)
        except ImportError:
            continue
        conf_module_name = "%s.conf" % app
        module = importlib.import_module(conf_module_name)
        PREFERENCES = getattr(module, "PREFERENCES", ())

        for preference in PREFERENCES:
            process_preference(preferences, preference, conf_module_name)
    
    for preference in conf.PREFERENCES:
        process_preference(preferences, preference, "settings")
    
    for kwargs in preferences.values():
        Property.objects.init_by(**kwargs)
