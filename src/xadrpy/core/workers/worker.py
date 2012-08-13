import logging
import os
import sys
import atexit
import threading
import signal
import time
import multiprocessing
from threading import Lock
from multiprocessing import Pipe

class Message(object):

    DEFAULT_PRIORITY=5
    
    def __init__(self, subject, message=None, headers={}, priority=DEFAULT_PRIORITY, id=None):
        import uuid
        self.subject = subject
        self.headers = headers
        self.message = message
        self.priority = priority
        self.id = id or str(uuid.uuid4())

    def reply(self, subject=None, message=None, headers={}, priority=None):
        return self.__class__(subject=subject or self.subject, message=message, headers=headers, id=self.id, priority=priority or self.DEFAULT_PRIORITY)

    def __repr__(self):
        return "<%s[%s]{%s} subject: %s>" % (self.__class__.__name__, self.priority, self.id, self.subject)

class DaemonMessage(Message):
    class SerializeException(Exception):
        pass

    @classmethod
    def loads(cls, raw_request):
        try: import json #@UnusedImport
        except: import simplejson as json #@Reimport
        try:
            request = json.loads(raw_request)
            instance = cls( id=request['id'], priority=request.get("priority",cls.DEFAULT_PRIORITY), subject = request['subject'], message = request.get('message'), headers = request.get('headers',{}) )
        except:
            raise DaemonMessage.SerializeException("Message deserialize error")
        return instance

    def dumps(self):
        try: import json #@UnusedImport
        except: import simplejson as json #@Reimport
        try:
            return json.dumps(dict(subject=self.subject, priority=self.priority, message=self.message, headers=self.headers, id=self.id))
        except:
            raise DaemonMessage.SerializeException("Message serialize error")
    
    def __str__(self):
        return self.dumps()

class DaemonExceptionMessage(DaemonMessage):
    def __init__(self, exception):
        super(DaemonExceptionMessage,self).__init__(subject="exception",priority=0, message=str(exception))


class DaemonMessageHandler(threading.Thread):
    
    def __init__(self):
        import Queue
        super(DaemonMessageHandler, self).__init__()
        self.daemon = True
        self.responders = {}
        self.queue = Queue.PriorityQueue()
        self.logger = logging.getLogger("MessageBusContainer")
    
    def addMessage(self, message):
        self.queue.put((1,message))
    
    def run(self):
        self.logger.info("Message handler started")
        while 1:
            message = self.queue.get()[1]
            self.trigger(message.subject, message)
        self.logger.info("Message handler stopped")
    
    def bind(self, subject, responder):
        if not subject in self.responders:
            self.responders[subject]=[]
        self.logger.debug("bind for "+subject+" messages")
        self.responders[subject].append(responder)
    
    def trigger(self, subject, message):
        if not subject in self.responders:
            return []
        self.logger.debug(subject+" message send to %s responders." % len(self.responders[subject]))
        return map(lambda responder: responder(message), self.responders[subject])
    
    def onRequest(self, request):
        return self.trigger(request.subject, request)
    
class DaemonSocketServer(threading.Thread):
    def __init__(self, socketfile, handler):
        super(DaemonSocketServer, self).__init__()
        import socket
        self.daemon = True
        self.socketfile = socketfile
        self.handler = handler
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.socketfile)
        self.socket.listen(5)
        self.logger = logging.getLogger("SocketServerContainer")
    
    def run(self):
        self.logger.info("Socket server started")
        while 1:
            self.connection = self.socket.accept()[0]
            raw_request = self.connection.recv(4096)
            try:
                request = DaemonMessage.loads(raw_request)
                if request.priority==0:
                    responses = self.handler.onRequest(request)
                    for response in responses:
                        if isinstance(response, DaemonMessage):
                            self.connection.send(response.dumps()+"\0")
                        elif response:
                            self.connection.send(str(response)+"\0")
                            
                else:
                    self.handler.addMessage(request)
            except Exception, e:
                self.connection.send(DaemonExceptionMessage(e).dumps()+"\0")
            self.connection.close()
        self.logger.info("Socket server stopped")    

class Worker( object ):
    
    def __init__( self, pidfile, socketfile, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null', decoupling=False, logger_name="Worker" ):
        self.pidfile = pidfile
        self.socketfile = socketfile
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.decoupling = decoupling
        self.running = False
        self.containers = []
        self.logger = logging.getLogger(logger_name)
        #self.running = threading.Event()
        #self.destroyed = threading.Event()

    
    def add_container(self, container):
        self.containers.append(container)

    def daemonize( self ):
        try:
            pid = os.fork()
            if pid > 0:
                os.waitpid(pid, 0)
                sys.stdout.flush()
                sys.exit( 0 )
        except OSError, e:
            sys.stderr.write( "fork #1 failed: %d (%s)\n" % ( e.errno, e.strerror ) )
            sys.exit( 1 )
            
        if self.decoupling:
            os.chdir( "/" )
            os.setsid()
            os.umask( 0 )
        try:
            parent, self.start_pipe = Pipe()
            pid = os.fork()
            if pid > 0:
                sys.stdout.write(parent.recv()+"\n")
                sys.exit( 0 )
        except OSError, e:
            sys.stderr.write( "fork #2 failed: %d (%s)\n" % ( e.errno, e.strerror ) )
            sys.exit( 1 )

        sys.stdout.flush()
        sys.stderr.flush()
        si = file( self.stdin, 'r' )
        so = file( self.stdout, 'a+' )
        se = file( self.stderr, 'a+', 0 )
        os.dup2( si.fileno(), sys.stdin.fileno() )
        os.dup2( so.fileno(), sys.stdout.fileno() )
        os.dup2( se.fileno(), sys.stderr.fileno() )

        atexit.register( self.delpid )
        pid = str( os.getpid() )
        file( self.pidfile, 'w+' ).write( "%s\n" % pid )
        

    def delpid( self ):
        os.remove( self.pidfile )
        os.remove( self.socketfile )
        
    def start( self ):

        try:
            pf = file( self.pidfile, 'r' )
            pid = int( pf.read().strip() )
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Worker already running?\n"
            raise Exception(message % self.pidfile)

        if os.path.exists(self.socketfile):
            os.remove(self.socketfile)
        self.daemonize()
        self.logger.info("Worker started, daemonized")
        try:
            self.run()
        except Exception:
            self.logger.exception("General exception")
        finally:
            self.logger.info("Destroying daemon...")
            self.onDone()
            self.logger.info("Shutdown process finished.")
    
    def onShutdown(self, message):
        self.logger.info("Starting shutdown process")
        self.interrupted.set()
    
    def onStatus(self, message):
        self.logger.debug("Catch 'status' message")
        return message.reply(subject="Running" if not self.interrupted.isSet() else "Interrupted")
        
    def makeContainers(self):
        def makeContainer(container):
            context = {}
            return container.make(context, self.interrupted)
        self.logger.info("Making %s containers..." % len(self.containers))
        self.containers = map(makeContainer, self.containers)
        
    def startContainers(self):
        def startContainer(container):
            self.logger.debug("Starring '%s' container..." % container.__class__.__name__)
            container.start()
            container.created.wait()
            if container.destroyed.isSet():
                raise Exception("'%s' container faild to start" % container.__class__.__name__)
        self.logger.info("Starting %s containers" % len(self.containers))
        map(startContainer, self.containers)
    
    def interruptContainers(self):
        def interruptContainer(container):
            if not container.destroyed.isSet():
                self.logger.debug("wait for %s container interruption..." % container.__class__.__name__)
                if not container.interrupt(60):
                    self.logger.error("%s container interruption timeout" % container.__class__.__name__)
                self.logger.error("%s container interrupted" % container.__class__.__name__)
                
        livingContainerCount = self.livingContainerCount()
        if livingContainerCount:
            self.logger.info("Interrupt %s containers" % livingContainerCount)
            interruption=[threading.Thread(target=interruptContainer, args=[container]) for container in self.containers]
            map(lambda i: i.start(), interruption)
            map(lambda i: i.join(), interruption)
    
    def livingContainerCount(self):
        i=0
        for container in self.containers:
            if container.running.isSet():
                i+=1
        return i
    
    def hasRunningContainers(self):
        hasRunning = False
        for container in self.containers:
            hasRunning|=container.running.isSet()
        return hasRunning
    
    def run(self):

        def stop(signo, frame):
            self.logger.warn("Stop by 'SIGTERM'")
            self.interrupted.set()
        
        self.interrupted = threading.Event() 
        
        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGUSR1, lambda signo,frame: self.onReload())
        signal.signal(signal.SIGUSR2, lambda signo,frame: self.onSync())
        
        self.messageHandler = DaemonMessageHandler()
        self.messageHandler.start()
        
        self.messageHandler.bind("shutdown", self.onShutdown)
        self.messageHandler.bind("status", self.onStatus)

        self.socketServer = DaemonSocketServer(self.socketfile, self.messageHandler)
        self.socketServer.start()
        
        time.sleep(1)
        self.logger.info("Server initialized")
        self.onInit()

        try:
            self.makeContainers()
        except:
            self.interrupted.set()
            self.start_pipe.send("Starting failed")
            self.logger.exception("Making container failed")
            self.onDone()
            return

        
        try:
            self.startContainers()
        except Exception, e:
            self.interrupted.set()
            self.start_pipe.send("Starting failed")
            self.logger.critical(e)
            self.logger.critical("Containers startup faild")
            self.interruptContainers()
            return
        self.logger.info("Server started")
        self.start_pipe.send("Started")
        self.onRun()
        self.interrupted.set()

        self.logger.info("Server stopped")
        
        self.interruptContainers()
    
    def onInit(self):
        pass
    
    def onRun(self):
        while not self.interrupted.isSet():
            time.sleep(5)
            if not self.hasRunningContainers():
                self.logger.warn("All containers stopped")
                self.interrupted.set()
    
    def onDone(self):
        pass
    
    def onReload(self):
        self.logger.info("Catch 'reload' signal")
        pass
    
    def onSync(self):
        self.logger.info("Catch 'sync' signal")
        pass
