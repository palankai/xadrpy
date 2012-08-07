'''
Created on 2012.06.27.

@author: pcsaba
'''
from django.core.urlresolvers import reverse
from xadrpy.access.models import Consumer
from django.dispatch.dispatcher import receiver
from xadrpy.utils.signals import application_started

#@todo: Ezt at kell emelni init/reset commandokba
#@receiver(application_started)
#def account_generate_key(**kwargs):
#    Consumer.objects.create_static("backoffice", "Back Office")
