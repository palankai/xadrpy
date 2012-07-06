import logging
logger = logging.getLogger("Auth")

class PermissionManager(object):
    
    def __init__(self):
        self._permissions = []
    
    def register(self, name, description=""):
        self._permissions.append((name, description))
        
    def get_permissions(self):
        return self._permissions

permissions = PermissionManager()
