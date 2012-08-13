from libs import Plugin
from models import SnippetInstance
from django.template.context import Context

class SnippetPlugin(Plugin):
    alias = "x-snippet"
    model = SnippetInstance
        
    def render(self, context):
        obj = self.get_plugin_instance()
        return self.get_template().render({})

class Pager(Plugin):
    alias = "x-pager"
    template = "xadrpy/plugins/pager.html"
    
    def render(self, context, paginated):
        if not paginated.need_pager:
            return ""
        ctx = Context({
            'paginated': paginated,
        })
        return self.get_template().render(ctx)
