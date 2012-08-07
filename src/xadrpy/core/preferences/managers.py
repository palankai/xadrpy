from django.db import models
from django.utils.translation import get_language
from django.contrib.sites.models import Site

class PrefManager(models.Manager):

    def find_by(self, **kwargs):
        if 'language_code' in kwargs:
            kwargs['language_code'] = self.fallback_language_code(kwargs['language_code'])
        if 'site' in kwargs:
            kwargs['site'] = self.fallback_site(kwargs['site'])
        return self.filter(**kwargs)

    def get_or_create_by(self, key=None, site=None, group=None, user=None, namespace=None, language_code=None):
        language_code, site = self.fallback(language_code, site)
        return self.get_or_create(site=site, group=group, user=user, namespace=namespace, key=key, language_code=language_code)

    def get_by(self, key=None, site=None, group=None, user=None, namespace=None, language_code=None):
        language_code, site = self.fallback(language_code, site)
        try:
            return self.get(key=key, site=site, group=group, user=user, namespace=namespace, language_code=language_code)
        except self.model.DoesNotExist:
            return None

    def init_by(self, value, key=None, site=None, group=None, user=None, namespace=None, language_code=None, meta=None, trans={}):
        pref, created = self.get_or_create_by(key=key, site=site, group=group, user=user, namespace=namespace, language_code=language_code)
        if created:
            pref.set_initial_value(value, meta=meta)
            for trans_language_code, kwargs in trans.items():
                pref.set_initial_alternative(language_code=trans_language_code, **kwargs)

    def fallback(self, language_code, site):
        language_code = self.fallback_language_code(language_code)
        site = self.fallback_site(site)
        return language_code, site


    def fallback_language_code(self, language_code):
        if language_code=="": 
            language_code=get_language()
        return language_code
    
    def fallback_site(self, site):
        if site==0:
            site = Site.objects.get_current()
        if type(site) == int:
            site = Site.objects.get(pk=site)
        return site
