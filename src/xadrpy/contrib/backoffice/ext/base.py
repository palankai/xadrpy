from django.utils.safestring import mark_safe

class JSFunction(object):
    def __init__(self, args, body):
        self.args = args
        self.body = body
    
    def to_js(self):
        return mark_safe("function(%s){%s}" % (",".join(self.args), self.body))
    
    def as_json(self):
        return "function(%s){%s}" % (",".join(self.args), self.body)
    
    @staticmethod
    def use(value):
        return value.to_js() if isinstance(value, JSFunction) else value

