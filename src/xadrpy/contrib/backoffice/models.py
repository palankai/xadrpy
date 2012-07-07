'''
Created on 2012.06.27.

@author: pcsaba
'''
from django.core.urlresolvers import reverse
from xadrpy.auth.models import Consumer

Consumer.objects.create_static("backoffice", "Back Office")
