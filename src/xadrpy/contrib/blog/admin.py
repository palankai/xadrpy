from django.contrib.admin import site, ModelAdmin
from models import Column, Category, Post
from django.utils.translation import ugettext_lazy as _ 

class PostAdmin(ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('column','title', 'slug', 'categories')
        }),
        (None, {
            'fields': ('content','excerpt', 'excerpt_image')
        }),
        (_("SEO"), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords','meta_robots','meta_cannonical')
        }),
        (_('Publication'), {
            'fields': ('user', 'group', 'status','publication', 'publication_end', 'source', 'source_url')
        }),
        (_('Relations'), {
            'fields': ('posts', 'pages')
        }),
        (_('Extra'), {
            'fields': ('weight', 'is_featured', 'layout', 'extra_classes', 'view_count', 'enable_comments')
        }),
    )
    list_display = ('column', 'title', 'created', 'user', 'status',)
    list_display_links = ('title', )
    list_filter = ('column', 'user')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)
    actions = ['make_published']
    
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='PUB')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_published.short_description = "Mark selected stories as published"            

site.register(Column)
site.register(Category)

site.register(Post, PostAdmin)
