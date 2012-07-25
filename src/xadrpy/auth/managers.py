from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import get_language

class PropertyManager(models.Manager):
    
    def __init__(self, consumer_cls, instance_cls, role_cls):
        super(PropertyManager, self).__init__()
        self.consumer_cls = consumer_cls
        self.instance_cls = instance_cls
        self.role_cls = role_cls
    
    def get_or_create_by(self, key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None):
        language_code, site, consumer, instance, role, custom_ct, custom_id = self.fallback(language_code, site, consumer, instance, role, custom)
        return self.get_or_create(instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom_ct=custom_ct, custom_id=custom_id, namespace=namespace, key=key, language_code=language_code) #@UnusedVariable
    
    def get_by(self, key=None, instance=None, site=None, consumer=None, account=None, rule=None, role=None, group=None, user=None, access=None, token=None, custom=None, namespace=None, language_code=None):
        language_code, site, consumer, instance, role, custom_ct, custom_id = self.fallback(language_code, site, consumer, instance, role, custom)
        try:
            return self.get(key=key, instance=instance, site=site, consumer=consumer, account=account, rule=rule, role=role, group=group, user=user, access=access, token=token, custom_ct=custom_ct, custom_id=custom_id, namespace=namespace, language_code=language_code)
        except self.model.DoesNotExist:
            return None
    
    def init_by(self, value, key=None, instance=None, site=None, consumer=None, role=None, namespace=None, language_code=None, title=None, description=None, meta=None, status=None, vtype=None, init=False, debug=False, trans={}):
        prop, created = self.get_or_create_by(key=key, instance=instance, site=site, consumer=consumer, role=role, namespace=namespace, language_code=language_code)
        rewrite = created or init or settings.DEBUG and debug
        if rewrite:
            prop.set_initial_value(value, title=title, description=description, meta=meta, status=status, vtype=vtype)
        
        for trans_language_code, kwargs in trans.items():
            prop.set_initial_alternative(language_code=trans_language_code, rewrite=rewrite, **kwargs)
        
    def fallback(self, language_code, site, consumer, instance, role, custom):
        if language_code=="": 
            language_code=get_language()
        if site==0:
            site = Site.objects.get_current()
        if type(consumer) == str:
            consumer=self.consumer_cls.objects.get_static(consumer, site=site)
        if type(instance) == str:
            instance=self.instance_cls.objects.get(key=instance)
        if type(role) == str:
            role=self.role_cls.objects.get(key=role)
        if type(site) == int:
            site = Site.objects.get(pk=site)
        custom_ct = None
        custom_id = None
        if custom:
            custom_ct = ContentType.objects.get_for_model(custom)
            custom_id = custom.id
        return language_code, site, consumer, instance, role, custom_ct, custom_id

class ConsumerManager(models.Manager):
    
    def create_static(self, static_key, name, site=None, description=None, redirect_uri=None, consumer_type=None, scope=[], data=None):
        consumer, unused = self.get_or_create(static_key=static_key, site=site)
        consumer.name = name
        consumer.site = site
        consumer.description = description
        consumer.redirect_uri = redirect_uri
        consumer.consumer_type = consumer_type
        consumer.scope = scope
        consumer.save()
        if data:
            consumer.set_initial_data(data)
        return consumer
    
    def get_static(self, static_key, site=None):
        return self.get(static_key=static_key, site=site)
