from xadrpy.contrib.plugins.base import Plugin

class CommentsPlugin(Plugin):
    alias = "x-feedback-comments"
    template = "xadrpy/plugins/feedback-comments.html"

    def __init__(self, entity, *args, **kwargs):
        self.entity = entity

    def render(self, context):
        context.update({
            'entity': self.entity
        })
        return self.render_template(context)
    