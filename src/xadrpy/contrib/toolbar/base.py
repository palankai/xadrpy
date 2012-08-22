from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils import simplejson 
import conf

class Toolbar(object):
    
    def __init__(self, request):
        self.request = request
        self.items = []
        self.switches = []
        self.plugins = []
        self.title = ""
        self.cookie = None
    
    def add(self, item):
        item.set_toolbar(self)
        self.items.append(item)
        
    def append_switch(self, switch):
        switch.set_toolbar(self)
        self.switches.append(switch)
    
    def append_plugin(self, plugin):
        plugin.set_toolbar(self)
        self.plugins.append(plugin)
    
    def set_title(self, title):
        self.title = title
        
    def get_cookie(self):
        if self.cookie is None:
            self.cookie = simplejson.loads(self.request.COOKIES.get(conf.COOKIE, "{}"))
        return self.cookie

class ToolbarItem(object):
    
    def set_toolbar(self, toolbar):
        self.toolbar = toolbar
    
    def render(self, context):
        pass

class ToolbarSwitch(ToolbarItem):
    
    def __init__(self, key, label, default=None, options=[]):
        self.key = key
        self.label = label
        self.default = default
        self.options = options
    
    def append(self, value, label, is_default=False):
        self.options.append((value, label,))
        if is_default:
            self.default = self.value
            
    def render(self, context):
        request = context['request']
        cookie = self.toolbar.get_cookie()
        values = dict(self.options)
        ctx = {
            'label': self.label,
            'key': self.key,
            'options': self.options,
            'next': request.get_full_path(),
            'current': values[cookie.get(self.key, self.default)]
        }
        return render_to_string("xadrpy/toolbar/toolbar-switch.html", ctx, context)

class ToolbarButton(ToolbarItem):
    
    def __init__(self, label, url, name="_self", opts={}, replace=True, question=None):
        self.label = label
        self.url = url
        self.name = name
        self.opts = opts
        self.replace = replace
        self.question = question
        self.menu = []
    
    def render(self, context):
        ctx = {
            'url': self.url,
            'label': self.label,
            'name': self.name,
            'replace': self.replace and 'true' or 'false',
            'opts': ",".join(["%s=%s" % a for a in self.opts.items()]),
            "menu": self.menu,
            "question": self.question,
        }
        return render_to_string("xadrpy/toolbar/toolbar-button.html", ctx, context)
