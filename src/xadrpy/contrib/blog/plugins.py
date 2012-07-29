from xadrpy.templates.libs import Plugin
from django.template.context import Context
from xadrpy.contrib.blog.models import Entry, Category
import logging
logger = logging.getLogger("x-blog")

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

class LatestEntriesPlugin(Plugin):
    alias = "x-blog-latest_entries"
    template = "xadrpy/blog/plugins/latest_entries.html"
    
    def render(self, context, router=None):
        entries = Entry.objects.get_entries()
        context.update({
            'router': router,
            'entries': entries
        })
        return self.get_template().render(context)

class CategoriesPlugin(Plugin):
    alias = "x-blog-categories"
    template = "xadrpy/blog/plugins/categories.html"

    def get_title(self):
        return "Categories"
    
    def has_title(self):
        return True

    def render(self, context, router=None):
        categories = Category.objects.all()
        categories[0].get_absolute_url()
        context.update({
            'categories': categories,
        })
        return self.get_template().render(context)
    