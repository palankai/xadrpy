from libs import Plugin
from models import SnippetInstance

class SnippetPlugin(Plugin):
    alias = "x-snippet"
    model = SnippetInstance
        
    def render(self, context):
        obj = self.get_plugin_instance()
        return self.get_template().render({})
