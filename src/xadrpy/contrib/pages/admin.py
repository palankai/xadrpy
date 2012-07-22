from django.contrib.admin import site, ModelAdmin
from models import Page

class PageAdmin(ModelAdmin):
    pass

site.register(Page, PageAdmin)
