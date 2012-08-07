from django import template
from django.utils.encoding import smart_str
import re
from django.template.base import FilterExpression, NodeList
from django.template.loader import get_template
from xadrpy.management.libs import SubCommand

kwarg_re = re.compile( r"(?:(\w+)=)?(.+)" )
class WidgetLibrary(template.Library):

    def widget_tag_compile_function(self, cls, widget_name):
        def widget_tag(parser, token):
            """
            {% xwidget 'valami nev' %}
            {% xwidget 'valami nev' as valtozo %}
            {% xwidget 'valami nev' with 'template.html' as valtozo %}
            {% xwidget 'valami nev' with variable as valtozo %}
            {% xwidget 'valami nev' with-inline as valtozo %}...{% endxwidget %}
            {% xwidget 'valami nev' with-inline %}...{% endxwidget %}
            """
            bits = token.split_contents()
            #widget_name = parser.compile_filter(bits[1])
            args = []
            kwargs = {}
            asvar = None
            templ = None
            bits = bits[1:]
            if len( bits ) >= 2 and bits[-2] == 'as':
                asvar = bits[-1]
                bits = bits[:-2]
            if len( bits ) >=1 and bits[-1] == 'with-inline':
                templ = True
                bits = bits[:-1]
            elif len( bits ) >=2 and bits[-2] == 'with':
                templ = bits[-1]
                bits = bits[:-2]
            if len( bits ):
                for bit in bits:
                    match = kwarg_re.match( bit )
                    if not match:
                        raise template.TemplateSyntaxError( "Malformed arguments to widget tag" )
                    name, value = match.groups()
                    if name:
                        kwargs[name] = parser.compile_filter( value )
                    else:
                        args.append( parser.compile_filter( value ) )
            if templ == True:
                templ = parser.parse(('end'+widget_name,))
                parser.delete_first_token()
            elif templ:
                templ = parser.compile_filter( templ )
                
            return cls(args, kwargs, templ, asvar)
        return widget_tag
    
    def widget(self, name):
        def inner(cls):
            self.tag(name, self.widget_tag_compile_function(cls, name))
        return inner

class XWidgetBase(template.Node):
    def __init__(self, args, kwargs, template, asvar):
        self.args = args
        self.kwargs = kwargs
        self.template = template
        self.asvar = asvar

    def render(self, context):
        def resolve(v, context):
            if unicode(v)==u"False": return False
            elif unicode(v)==u"True": return True
            elif unicode(v)==u"None": return None
            else:
                return v.resolve(context)
        args = [arg.resolve( context ) for arg in self.args]
        kwargs = dict( [( smart_str( k, 'ascii' ), resolve(v, context) ) for k, v in self.kwargs.items()] )
        
        if isinstance(self.template, FilterExpression):
            kwargs['TEMPLATE']=get_template(self.template.resolve( context ))
        if isinstance(self.template, NodeList):
            kwargs['TEMPLATE']=self.template
        
        if not self.asvar:
            return self.value(context, *args, **kwargs)
        
        context[self.asvar]=self.value(context, *args, **kwargs)
        return ""
    
    def value(self, context, *args, **kwargs):
        return ""


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
    
    def has_title(self):
        return False

    def get_title(self):
        return None
    
    def get_plugin_instance(self):
        return self.model.objects.get_or_create(plugin=self.get_name(), placeholder=self.placeholder, page=self.page)[0]
    
    def render(self, config, *args, **kwargs):
        pass

class TemplatesCommands(SubCommand):

    def register(self):
        _init = self.command.add_subcommand(self.init, "templates.init", help="Init templates, plugins, ...")

    def reset(self, **kwargs):
        from xadrpy.templates.models import PluginStore
        PluginStore.objects.all().delete()
        self.init(**kwargs)

    def init(self, **kwargs):
        import imp
        from django.utils import importlib
        from django.conf import settings
        from inspect import isclass
        from models import PluginStore
        
        for app in settings.INSTALLED_APPS:
            
            try:                                                                                                                          
                app_path = importlib.import_module(app).__path__                                                                          
            except AttributeError:                                                                                                        
                continue 
            
            try:                                                                                                                          
                imp.find_module('plugins', app_path)                                                                               
            except ImportError:                                                                                                           
                continue                                                                                                                  
            module = importlib.import_module("%s.plugins" % app)
            for name in dir(module):
                cls = getattr(module,name)
                if isclass(cls) and issubclass(cls, Plugin) and cls!=Plugin:
                    store = PluginStore.objects.get_or_create(plugin=cls.get_name())[0]
