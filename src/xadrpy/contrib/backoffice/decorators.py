from xadrpy.core.api.decorators import APIInterface
from xadrpy.contrib.backoffice.generic import store_manager, model_manager

class BackOfficeInterface(APIInterface):

    def __init__(self, prefix, namespace):
        super(BackOfficeInterface, self).__init__(prefix)
        self.namespace = namespace

    def register_store(self, obj, pattern=None):
        self.register_object(obj, pattern)
        store_manager.register(obj)

    def register_model(self, obj, pattern=None):
        self.register_object(obj, pattern)
        model_manager.register(obj)
