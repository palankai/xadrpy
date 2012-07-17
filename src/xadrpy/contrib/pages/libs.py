from django.template.base import Template
from django.template.context import Context
from django.template.loader import get_template

PLUGIN_CACHE = {}

class Plugin(object):
    title = "Plugin"
    description = ""
    alias = None
    model = None
    template = None

    def __init__(self, placeholder, page=None):
        self.placeholder = placeholder
        self.page = page
    
    def init_template(self, template):
        if template:
            self.template = template
        elif isinstance(self.template, str):
            self.template = get_template(self.template)
    
    def get_template(self):
        return self.template
    
    @classmethod
    def get_name(cls):
        return "%s.%s" % (cls.__module__, cls.__name__)
    
    def get_plugin_instance(self):
        return self.model.objects.get_or_create(plugin=self.get_name(), placeholder=self.placeholder, page=self.page)[0]
    
    def render(self, config, *args, **kwargs):
        pass
