from base import Plugin

class Pager(Plugin):
    alias = "x-pager"
    template = "xadrpy/plugins/pager.html"

    def __init__(self, paginated, *args, **opts):
        self.paginated = paginated
        Plugin.__init__(self, *args, **opts)
    
    def init(self, context):
        if not self.paginated.need_pager:
            self.visible = False
    
    def render(self, context):
        context.update({
            'paginated': self.paginated,
        })
        return self.render_template(context)
