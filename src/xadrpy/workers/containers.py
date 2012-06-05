import sys, os, time, atexit
import signal
import threading, logging

from exceptions import InterruptedException


class Container(threading.Thread):
    def __init__(self, context, idle_time=0, group=None, name=None, parent_interrupted=None):
        super(Container, self).__init__(group=group, name=name)
        self.idle_time = idle_time
        self.daemon = True
        
        self._init_context(context)
        self._init_events()
        self._init_logger()
        self._init_parent_interrupted(parent_interrupted)
        
    
    def _init_context(self, context):
        self.context = context
        
    def _init_events(self):
        self.created = threading.Event()
        self.running = threading.Event()
        self.destroyed = threading.Event()
        self.interrupted = threading.Event()
        
    def _init_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Borned")
        
    def _init_parent_interrupted(self, parent_interrupted):
        def wait_for_parent(event):
            event.wait()
            self.interrupted.set()
            self.logger.debug("Parent interrupted")
        if parent_interrupted:
            waiting = threading.Thread(target=wait_for_parent, args=[parent_interrupted])
            waiting.daemon = True
            waiting.start()
            self.logger.info("Start parent interrupting observation")

    def sleep(self, idle_time=None, raise_exception=True):
        self.interrupted.wait(idle_time or self.idle_time or 0)
        if self.interrupted.isSet():
            if raise_exception: 
                raise InterruptedException()

    def interrupt(self, timeout=None):
        if self.destroyed.isSet(): return True
        self.logger.info("Send interrupted")
        self.interrupted.set()
        self.destroyed.wait(timeout)
        return self.destroyed.isSet()
        
    def run(self):
        self.logger.info("Prepare to start")
        try: 
            self.on_create()
            self.sleep(0)
        except InterruptedException:
            self.interrupted.set()
            self.destroyed.set()
            self.created.set()
        except:
            self.logger.exception("Creation failed!")
            self.interrupted.set()
            self.destroyed.set()
            self.created.set()
            return
            
        self.created.set()
        self.logger.info("Created")
        self.running.set()
        self.logger.info("Started")
        try:
            self.sleep()
            self.on_process()
            self.logger.info("Process is done bye normal way")
        except InterruptedException:
            self.logger.info("Process interrupted")
        except Exception:
            self.logger.exception("Interrupted by an exception")
        self.running.clear()
        self.interrupted.set()
        try: 
            self.on_destroy()
        except:
            self.logger.exception("Destroying failed!")
        finally:
            self.destroyed.set()
        self.logger.info("Destroyed")        
    
    @classmethod
    def make(cls, context, parent_interrupted):
        return cls(context, parent_interrupted=parent_interrupted)    
    
    def on_create(self):
        pass
    
    def on_process(self):
        pass
    
    def on_destroy(self):
        pass
    
