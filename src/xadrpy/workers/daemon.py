import logging
import os
import sys
import atexit
import threading
import signal
import time
import socket
from multiprocessing import Pipe
from xadrpy.workers.lib import get_container_class
from conf import CONTAINERS

class DaemonError( Exception ): pass
class DaemonAlreadyRunningException( DaemonError ): pass
class DaemonNotRunningException( DaemonError ): pass

class DaemonContainer( object ):
    
    def __init__(self, environment):
        self.environment = environment
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def on_start(self):
        pass
    
    def on_stop(self):
        pass
    
    def on_reload(self):
        pass
    
    def on_sync(self):
        pass
    
    def on_status(self):
        pass
    
    def on_message(self, message):
        pass

class Daemon( object ):
    
    def __init__( self, pidfile, socketfile, pipe, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null', decoupling=False, logger_name="Daemon" ):
        self.pidfile = pidfile
        self.socketfile = socketfile
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.decoupling = decoupling
        self.pipe = pipe
        self.running = False
        self.logger = logging.getLogger(logger_name)
        self.push_bootstrapping_status("CREATED")

    def get_pid(self):
        try:
            pf = file( self.pidfile, 'r' )
            pid = int( pf.read().strip() )
            pf.close()
        except IOError:
            pid = None
        return pid

    def daemonize( self ):
        try:
            pid = os.fork()
            if pid > 0:
                self.push_bootstrapping_status("FORK1")
                sys.exit( 0 )
        except OSError, e:
            msg = "fork #1 failed: %d (%s)\n" % ( e.errno, e.strerror )
            self.logger.exception(msg)
            sys.stderr.write( msg )
            sys.exit( 1 )
        
        if self.decoupling:
            os.chdir( "/" )
            os.setsid()
            os.umask( 0 )
        try:
            pid = os.fork()
            if pid > 0:
                self.push_bootstrapping_status("FORK2", pid)
                sys.exit( 0 )
        except OSError, e:
            msg = "fork #2 failed: %d (%s)\n" % ( e.errno, e.strerror )
            self.logger.exception(msg)
            sys.stderr.write( msg )
            sys.exit( 1 )

        sys.stdout.flush()
        sys.stderr.flush()
        si = file( self.stdin, 'r' )
        so = file( self.stdout, 'a+' )
        se = file( self.stderr, 'a+', 0 )
        os.dup2( si.fileno(), sys.stdin.fileno() )
        os.dup2( so.fileno(), sys.stdout.fileno() )
        os.dup2( se.fileno(), sys.stderr.fileno() )

        atexit.register( self._del_pid )
        pid = str( os.getpid() )
        file( self.pidfile, 'w+' ).write( "%s\n" % pid )

    def _del_pid( self ):
        os.remove( self.pidfile )
        if os.path.exists(self.socketfile):
            os.remove( self.socketfile )

    def start( self ):
        self.push_bootstrapping_status("STARTING")

        pid = self.get_pid()
    
        if pid:
            raise DaemonAlreadyRunningException("Daemon pidfile %s already exist." % self.pidfile)

        if os.path.exists(self.socketfile):
            os.remove(self.socketfile)
        self.daemonize()
        self.interrupted = threading.Event()

        signal.signal(signal.SIGTERM, lambda signo, frame: self.on_SIGTERM())
        signal.signal(signal.SIGUSR1, lambda signo, frame: self.on_reload())
        signal.signal(signal.SIGUSR2, lambda signo, frame: self.on_sync())


        self.logger.info("Worker started.")

        try:
            #self.start_socket_server(self.socketfile)
            self.push_bootstrapping_status("STARTING_SERVICES")
            self.on_start()
            self.logger.info("Services started.")
            self.push_bootstrapping_status("STARTED")
            while not self.interrupted.is_set():
                self.interrupted.wait(1)
            self.logger.info("Services stopping.")
        except Exception, e:
            self.logger.exception("General exception: %s" % e)
            self.push_bootstrapping_status("FAILED")
        finally:
            self.on_stop()
            self.logger.info("Shutdown process finished.")
    
    def on_start(self):
        pass
    
    def on_stop(self):
        pass

    def on_reload(self):
        pass
    
    def on_sync(self):
        pass

    def on_message(self, message):
        return "\n"

    def on_SIGTERM(self):
        self.logger.info("Interrupted")
        self.interrupted.set()

    def puss_service_starting(self, service_name):
        self.push_bootstrapping_status("SERVICE_STARTING",service_name)
    
    def puss_service_started(self, service_name):
        self.push_bootstrapping_status("SERVICE_STARTED",service_name)

    def puss_service_starting_failed(self, service_name):
        self.push_bootstrapping_status("SERVICE_ERROR",service_name)

    def push_bootstrapping_status(self, *args):
        try:
            self.pipe.send(":".join([str(arg) for arg in args])+"\n")
        except IOError, e:
            pass

    
#    def start_socket_server(self, socketfile_name):
#        socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#        socket.bind(socketfile_name)
#        socket.listen(5)
#        socket.setdefaulttimeout(5)
#        server_thread = threading.Thread(target=self.socket_server, args=(socket))
#        server_thread.daemon = True
#        server_thread.start()
#    
#    def socket_server(self, socket):
#        while not self.interrupted.is_set():
#            try: (client_socket, address) = socket.accept()
#            except socket.timeout: continue
#            raw_request = ""
#            while 1:
#                try: raw = client_socket.recv(1024)
#                except socket.timeout: continue
#                if not len(raw): break
#                raw_request += raw
#                parts = raw_request.split("\r\n")
#                raw_request=parts.pop()
#                for part in parts:
#                    try:
#                        response = self.on_message(part)
#                        if not isinstance(response, str):
#                            raise ValueError("Need string response")
#                    except Exception, e:
#                        self.logger.exception(str(e))
#                        response = "EXCEPTION"
#                    client_socket.sendall(response+"\r\n")
#            client_socket.close()

class ServiceError(DaemonError): pass
class ServiceAlreadyExists(ServiceError): pass
class ServiceDoesNotExists(ServiceError): pass
class ServiceIsRunning(ServiceError): pass
class ServiceIsNotRunning(ServiceError): pass

class DaemonInterface( object ):
    def __init__(self, daemon):
        self.daemon = daemon
        
    def get_services(self):
        return self.daemon.get_services()
        

class ComplexDaemon( Daemon ):

    def __init__(self, pidfile_name, socketfile_name, pipe, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null', decoupling=False, logger_name="Daemon"):
        Daemon.__init__(self, pidfile_name, socketfile_name, pipe, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null', decoupling=False, logger_name="ComplexDaemon")
        self.service_list = []
        self.services = {}
        self.interface = DaemonInterface(self)

    def on_start(self):
        self.logger.info("Starting services...")
        for service_name in self.service_list:
            try:
                self.logger.info("Starting %s service..." % (service_name, ))
                self.push_bootstrapping_status("SERVICE_STARTING",service_name)
                self.start_service(service_name)
                self.logger.info("%s service started." % (service_name, ))
                self.push_bootstrapping_status("SERVICE_STARTED",service_name)
            except Exception, e:
                self.logger.exception("Starting %s service failed: %s" % (service_name, str(e)))
                self.push_bootstrapping_status("SERVICE_ERROR",service_name)
   
    def on_stop(self):
        self.logger.info("Stopping services...")
        for service_name in self.service_list:
            try:
                self.logger.info("Stopping %s service..." % (service_name, ))
                self.stop_service(service_name)
                self.logger.info("%s service stopped." % (service_name, ))
            except Exception, e:
                self.logger.exception("Stopping %s service failed: %s" % (service_name, str(e)))
   
    def on_reload(self):
        self.logger.info("Reload services...")
        for service_name in self.service_list:
            try:
                self.logger.info("Reload %s service..." % (service_name, ))
                service = self.services[service_name]
                service.on_reload()
                self.logger.info("%s service reloaded." % (service_name, ))
            except Exception, e:
                self.logger.exception("Reloading %s service failed: %s" % (service_name, str(e)))

    def on_sync(self):
        self.logger.info("Syncing services...")
        for service_name in self.service_list:
            try:
                self.logger.info("Sync %s service..." % (service_name, ))
                self.service_stop(service_name)
                self.logger.info("%s service synced." % (service_name, ))
            except Exception, e:
                self.logger.exception("Syncing %s service failed: %s" % (service_name, str(e)))
    
    def add_service(self, service_name, service_class, env={}):
        if service_name in self.service_list:
            raise ServiceAlreadyExists(service_name)
        if isinstance(service_class, str):
            service_class = get_container_class(service_class)
        self.service_list.append(service_name)
        self.services[service_name] = {
            'service_name': service_name,
            'service_class': service_class,
            'environment': env,
            'instance': None,
            'running': threading.Event(),
            'status': None,
        }
        
    def remove_service(self, service_name):
        service = self.get_service(service_name)
        if service['running'].is_set():
            raise ServiceIsRunning(service_name)
        self.service_list.remove(service_name)
        del self.services[service_name]
        
    def start_service(self, service_name):
        service = self.get_service(service_name)
        if service['running'].is_set():
            raise ServiceIsRunning(service_name)
        service['running'].set()
        service['instance'] = service['service_class'](service['environment'])
        service['instance'].on_start()

    def stop_service(self, service_name):
        service = self.get_service(service_name)
        if not service['running'].is_set():
            raise ServiceIsNotRunning(service_name)
        #service['instance'] = service['service_class'](self.interface, service['environment'])
        service['instance'].on_stop()
        service['instance']=None
        service['status']=None
        service['running'].clear()
    
    def get_service(self, service_name):
        if service_name not in self.service_list:
            raise ServiceAlreadyExists(service_name)
        return self.services[service_name]
    

class BootstrapEventHandler( object ):
    
    def on_lost(self, left):
        if left:
            sys.stdout.write(" .")
        else:
            sys.stdout.write(" . losted\n")
        sys.stdout.flush()
    
    def on_ping(self):
        pass
    
    def on_init(self):
        sys.stdout.write("Starting...")
        sys.stdout.flush()
    
    def on_created(self):
        sys.stdout.write("C.")
        sys.stdout.flush()
    
    def on_starting(self):
        sys.stdout.write("S.")
        sys.stdout.flush()
    
    def on_fork1(self):
        sys.stdout.write("F1.")
        sys.stdout.flush()
    
    def on_fork2(self, daemon_pid=None):
        sys.stdout.write("F2(%s)." % daemon_pid)
        sys.stdout.flush()

    def on_starting_services(self):
        sys.stdout.write(" Phase 1 - Ok\n")
        sys.stdout.flush()

    def on_service_starting(self, service_name):
        sys.stdout.write(" - Service %s starting..." % service_name)
        sys.stdout.flush()
    
    def on_service_started(self, service_name):
        sys.stdout.write(" started.\n")
        sys.stdout.flush()

    def on_service_failed(self, service_name):
        sys.stdout.write(" starting failed.\n")
        sys.stdout.flush()
    
    def on_started(self):
        sys.stdout.write("Worker started. Phase 2 - Ok\n")
        sys.stdout.flush()
    
    def on_starting_failed(self):
        sys.stdout.write("Starting failed.\n")
        sys.stdout.flush()

class DaemonHandler( object ):
    
    def __init__(self, pidfile_name, socketfile_name, name = "Worker"):
        self.pidfile_name = pidfile_name
        self.socketfile_name = socketfile_name
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.reader_connection, self.writer_connection = Pipe(duplex=False)
        
    
    def start(self, decoupling=False, event_handler = BootstrapEventHandler()):
        pid = self._get_pid()
        if pid: raise DaemonAlreadyRunningException("%s is running." % self.name)
        
        event_handler.on_init()
        threading.Thread(target=self.start_handler, args=(self.reader_connection, event_handler)).start()

        daemon = ComplexDaemon(self.pidfile_name, self.socketfile_name, self.writer_connection)
        for service_name, service_class, env in CONTAINERS:
            daemon.add_service(service_name, service_class, env)

        daemon.start()
    
    def start_handler(self, connection, event_handler):
        while 1:
            has_data = False
            hops = 15
            while hops and not has_data:
                has_data = connection.poll(1)
                hops-=1
                if not has_data:
                    event_handler.on_lost(hops)
            if not has_data:
                break
            args = connection.recv().strip().split(":")
            status = args.pop(0)
            if status == "PING": event_handler.on_ping(*args)
            if status == "CREATED": event_handler.on_created(*args)
            if status == "STARTING": event_handler.on_starting(*args)
            if status == "FORK1": event_handler.on_fork1(*args)
            if status == "FORK2": event_handler.on_fork2(*args)
            if status == "STARTING_SERVICES": event_handler.on_starting_services(*args)
            if status == "SERVICE_STARTING": event_handler.on_service_starting(*args)
            if status == "SERVICE_STARTED": event_handler.on_service_started(*args)
            if status == "SERVICE_ERROR": event_handler.on_service_failed(*args)
            if status == "STARTED": 
                event_handler.on_started(*args)
                break
            if status == "FAILED": 
                event_handler.on_starting_failed(*args)
                break
        connection.close()
        
    def stop(self, force=False):
        pid = self._get_pid()
        if not pid:
            raise DaemonNotRunningException("%s is not running." % self.name)
        try:
            while 1:
                os.kill( pid, signal.SIGTERM )
                time.sleep( 0.1 )
        except OSError, err:
            err = str( err )
            if err.find( "No such process" ) > 0:
                if os.path.exists( self.pidfile_name ):
                    os.remove( self.pidfile_name )
                if os.path.exists( self.socketfile_name ):
                    os.remove( self.socketfile_name )
            else:
                raise DaemonError(err)
    
    def status(self):
        pid = self._get_pid()
        if pid:
            sys.stdout.write("%s is running. [%d]\n" % (self.name, pid))
        else:
            sys.stdout.write("%s is not running.\n" % self.name)
    
    def reload(self):
        pid = self._get_pid()
        if not pid:
            raise DaemonNotRunningException("%s is not running." % self.name)
        os.kill( pid, signal.SIGUSR1 )
    
    def sync(self):
        pid = self._get_pid()
        if not pid:
            raise DaemonNotRunningException("%s is not running." % self.name)
        os.kill( pid, signal.SIGUSR2 )
    
    def _get_pid(self):
        try:
            pf = file( self.pidfile_name, 'r' )
            pid = int( pf.read().strip() )
            pf.close()
        except IOError:
            pid = None
        return pid

if __name__ == "__main__":
    print "Start main()"
    daemon_handler = DaemonHandler("daemon.pid", "daemon.sock")
    try:
        daemon_handler.start()
    except DaemonError, e:
        sys.stderr.write("Error: "+str(e)+"\n")
            