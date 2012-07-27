from xadrpy.templates.libs import Plugin
from django.template.context import Context
from xadrpy.contrib.blog.models import Post

class PostsPlugin(Plugin):
    alias = "x-posts"
    template = "xadrpy/blog/plugins/posts.html"
        
    def render(self, context, posts):
        ctx = Context(context)
        ctx.update({
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

class LastEntriesPlugin(Plugin):
    alias = "x-last_entries"
    template = "xadrpy/blog/plugins/last_entries.html"
    
    def render(self, context, router=None):
        posts = Post.objects.all()
        context.update({
            'router': router,
            'posts': posts
        })
        return self.get_template().render(context)
        