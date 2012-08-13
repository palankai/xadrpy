from hashlib import sha512
from uuid import uuid4
import time
import datetime

class KeyGenerator(object):
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]

class TimestampGenerator(object):
    
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds

class ExpiredGenerator(object):
    
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return datetime.datetime.now() + datetime.timedelta(seconds=self.seconds) 

def check_authentication(request):
    pass