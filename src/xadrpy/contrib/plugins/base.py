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
    
    def init_inline(self, inline):
        self.inline = inline
    
    def init_template(self, template):
        if template:
            self.template = template
        if isinstance(self.template, basestring):
            self.template = get_template(self.template)

    def _get_renderable(self, template):
        if isinstance(template, basestring):
            return get_template(template)
        return template
        
    
    def get_template(self):
        if isinstance(self.template, basestring):
            self.template = get_template(self.template)
        return self.template
    
    def render_template(self, context={}, template=None):
        if template:
            return self._get_renderable(template).render(context)
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
        if not self.inline and not self.template:
            self.visible = False
    
    def render(self, context):
        """
        Render default template
        """
        context.update({
            'options': self.options,
            'args': self.args,
            'store': self.store,
            'place': self.place,
            'self': self,
        })
        return (self.get_template() or self.inline).render(context)
        #return self.template.render(context)
