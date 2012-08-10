from xadrpy.templates.libs import Plugin

class CategoriesPlugin(Plugin):
    alias = "x-feedback-comments"
    template = "xadrpy/plugins/feedback-comments.html"

    def get_title(self):
        return "Comments"
    
    def has_title(self):
        return True

    def render(self, context, router=None):
        context.update({
        })
        return self.get_template().render(context)
    