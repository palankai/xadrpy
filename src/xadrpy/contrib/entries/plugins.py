from xadrpy.core.templates.libs import Plugin
from django.template.context import Context
from models import Entry, Category
import logging
logger = logging.getLogger("x-blog")

class PostsPlugin(Plugin):
    alias = "x-posts"
    template = "xadrpy/entries/plugins/entries.html"
        
    def render(self, context, posts):
        ctx = Context(context)
        ctx.update({
            'posts': posts
        })
        return self.get_template().render(ctx)

class ArchivesPlugin(Plugin):
    alias = "x-archives"
    template = "xadrpy/entries/plugins/archives.html"
    
    def render(self, context, router=None):
        ctx = Context({
            'router': router,
        })
        return self.get_template().render(ctx)

class LatestEntriesPlugin(Plugin):
    alias = "x-entries-latest_entries"
    template = "xadrpy/entries/plugins/latest_entries.html"
    
    def render(self, context, router=None):
        entries = Entry.objects.get_entries()
        context.update({
            'router': router,
            'entries': entries
        })
        return self.get_template().render(context)

class CategoriesPlugin(Plugin):
    alias = "x-entries-categories"
    template = "xadrpy/entries/plugins/categories.html"

    def get_title(self):
        return "Categories"
    
    def has_title(self):
        return True

    def render(self, context, router=None):
        categories = Category.objects.get_active_categories()
        if not categories:
            return ""
        context.update({
            'categories': categories,
        })
        return self.get_template().render(context)
    