'''
Created on 2012.08.21.

@author: pcsaba
'''
from django.http import HttpResponseRedirect
import conf
from django.utils import simplejson
def toolbar(request):
    pass

def switch(request, key):
    value = request.GET.get('v')
    response = HttpResponseRedirect(request.GET.get('next', '/'))
    cookie = simplejson.loads(request.COOKIES.get(conf.COOKIE, "{}"))
    cookie[key]=simplejson.loads(value)
    response.set_cookie(conf.COOKIE, simplejson.dumps(cookie))
    return response 