
class APIObject(object):
    
    _public = []
    
    @classmethod
    def response(self, func=None, pattern=None, kwargs=None, root="response", successProperty="success", totalProperty="total", directionParam="direction", filterParam="filter", groupParam="group", limitParam="limit", pageParam="page", sortParam="sort", startParam="start", permissions=[]):
        pass
