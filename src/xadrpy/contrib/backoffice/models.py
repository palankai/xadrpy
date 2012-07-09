'''
Created on 2012.06.27.

@author: pcsaba
'''
from django.core.urlresolvers import reverse
from xadrpy.auth.models import Consumer
from django.db.models.signals import post_syncdb
from django.dispatch.dispatcher import receiver

@receiver(post_syncdb, sender=Consumer)
def account_generate_key(sender, instance, **kwargs):
    Consumer.objects.create_static("backoffice", "Back Office")
