from xadrpy.core.workers.daemon import DaemonContainer
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading

class XMLRPCContainer( DaemonContainer ):
    
    def __init__(self, environment):
        super(XMLRPCContainer, self).__init__(environment)
        self.address = (environment.get("host","localhost"), environment.get("port", 9001))
        self.server = SimpleXMLRPCServer(self.address)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server_thread = threading.Thread(self.server.serve_forever) 

    def on_start(self):
        self.server_thread.stop()
    
    def on_stop(self):
        self.server.shutdown()
        
    def register_service(self, name, method):
        pass


