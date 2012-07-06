'''
Created on 2012.06.27.

@author: pcsaba
'''
from django.core.urlresolvers import reverse
from xadrpy import api

api.models.Client.objects.create_static_client("backoffice", "Back Office")
