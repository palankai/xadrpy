from conf import *

def autodiscover():
    from xadrpy.utils.signals import autodisvover_signal, application_started
    autodisvover_signal.send(None)
    application_started.send(None)
