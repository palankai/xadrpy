from django.contrib.admin.options import ModelAdmin

class Plugin(ModelAdmin):

    def __init__(self, *args, **kwargs):
        pass
    
    def render(self, context):
        pass

class Menu(Plugin):
    pass