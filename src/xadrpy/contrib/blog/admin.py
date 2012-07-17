from django.contrib.admin import site, ModelAdmin
from models import Column, Category, Post
from django.utils.translation import ugettext_lazy as _ 

class PostAdmin(ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'categories', 'column')
        }),
        (_('Publication'), {
            'fields': ('author', 'author_group', 'status','publication', 'publication_end', 'source', 'source_title')
        }),
        (_('Relations'), {
            'fields': ('posts', 'pages')
        }),
        (_('Extra'), {
            'fields': ('weight', 'is_featured', 'layout', 'extra_classes', 'view_count', 'enable_comments')
        }),
        (None, {
            'fields': ('excerpt_image', 'excerpt', 'content',)
        }),
    )
    list_display = ('column', 'title', 'created', 'author', 'status',)
    list_display_links = ('title', )
    list_filter = ('column', 'author')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)

site.register(Column)
site.register(Category)

site.register(Post, PostAdmin)
