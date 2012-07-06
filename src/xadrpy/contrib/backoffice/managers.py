from django.db.models import Manager

class BackOfficeManagerMixin(object):
    
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

class BackOfficeManager(Manager, BackOfficeManagerMixin):
    pass
