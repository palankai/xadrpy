from conf import *
from xadrpy.utils.signals import autodiscover_signal, application_started

def autodiscover():
    autodiscover_signal.send(None)
    application_started.send(None)
    
