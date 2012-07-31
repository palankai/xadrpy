from conf import *
_CALLED = False

def autodiscover():
    global _CALLED
    if _CALLED: return
    _CALLED = True
    
    from xadrpy.utils.signals import autodiscover_signal, application_started
    autodiscover_signal.send(None)
    application_started.send(None)
    
