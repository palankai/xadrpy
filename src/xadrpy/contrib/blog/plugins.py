from xadrpy.contrib.pages.libs import Plugin
from django.template.context import Context

class PostsPlugin(Plugin):
    alias = "x-posts"
    template = "xadrpy/blog/plugins/posts.html"
        
    def render(self, context, posts):
        ctx = Context({
            'posts': posts
        })
        return self.get_template().render(ctx)

class ArchivesPlugin(Plugin):
    alias = "x-archives"
    template = "xadrpy/blog/plugins/archives.html"
    
    def render(self, context, router=None):
        ctx = Context({
            'router': router,
        })
        return self.get_template().render(ctx)
        