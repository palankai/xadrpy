from django.template.loader import get_template

class Plugin(object):
    alias = None
    title = "Plugin"
    description = ""
    template = None
    visible = True
    model = None

    def __init__(self, *args, **options):
        self.args = args
        self.options = options
        self.store = None
        self.place = None
    
    def set_store(self, store):
        self.store = store
        
    def set_place(self, place):
        self.place = place
    
    def init_template(self, template):
        if template:
            self.template = template
        if isinstance(self.template, basestring):
            self.template = get_template(self.template)
    
    def get_template(self):
        return self.template
    
    def render_template(self, context={}):
        return self.get_template().render(context)
    
    @classmethod
    def get_name(cls):
        return "%s.%s" % (cls.__module__, cls.__name__)
    
    def is_visible(self):
        return self.visible
    
    def init(self, context):
        """
        Run just before render() called
        The best place for define it is visible at the moment or not
        """
        pass
    
    def render(self, context):
        """
        Render default template
        """
        context.update({
            'options': self.options,
            'args': self.args,
            'store': self.store,
            'place': self.place
        })
        return self.template.render(context)
