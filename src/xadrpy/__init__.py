from conf import *

def autodiscover():
    from xadrpy.utils.signals import autodiscover_signal, application_started
    autodiscover_signal.send(None)
    application_started.send(None)
