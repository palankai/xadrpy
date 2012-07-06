
from django.db.models import Manager

class APIManagerMixin(object):
    
    def apply_request(self, request, need_total=False):
        query_set = self.get_query_set()
        
        if request.PARAMS.orders:
            query_set = query_set.order_by(*request.PARAMS.orders)
        if request.PARAMS.filters:
            query_set = query_set.filter(**request.PARAMS.filters)
        
        if need_total:
            total = query_set.count()
            
        if request.PARAMS.start:
            query_set = query_set[request.PARAMS.start:]
        if request.PARAMS.limit:
            query_set = query_set[:request.PARAMS.limit]
        if need_total:
            return query_set, total
        return query_set

class APIManager(Manager, APIManagerMixin):
    pass

class ClientManager(Manager):
    
    def create_static_client(self, static_key, name, redirect_uri=None, client_type=None, scope=[], data={}):
        client, created = self.get_or_create(static_key=static_key)
        client.name = name
        client.client_type = client_type
        client.redirect_uri = redirect_uri
        client.scope = scope
        client.data = data
        if created:
            client.generate_keys(save=False)
        
        client.save()
        
        return client
    
    def get_static_client(self, static_key):
        return self.get(static_key = static_key)

class AccessManager(Manager):
    
    
    pass

class TokenManager(Manager):
    pass