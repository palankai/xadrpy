# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

class IllegalWrapperOption(Exception): pass

class IllegalServiceOption(Exception): pass

class ServiceException(Exception):
    def __init__(self, message, e, response, status):
        self.status = status
        self.response = response
        self.e = e
        Exception.__init__(self, message)


class UnAuthorizedRequest(Exception):
    status = 403
    def __init__(self, message=_("Unauthorized request"), *args):
        Exception.__init__(self, message, *args)
