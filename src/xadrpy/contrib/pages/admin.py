from django.contrib.admin import site, ModelAdmin
from models import Root, Page, Post

site.register(Root)
site.register(Page)
site.register(Post)
