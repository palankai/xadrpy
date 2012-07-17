from django import template
from django.template.loader import get_template
from django.utils.encoding import smart_str
import re
from django.template.base import FilterExpression, NodeList

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
            if len( bits ) < 2:
                raise template.TemplateSyntaxError( "'%s' takes at least one argument (widget_name)" % bits[0] )
            #widget_name = parser.compile_filter(bits[1])
            args = []
            kwargs = {}
            asvar = None
            template = None
            bits = bits[1:]
            if len( bits ) >= 2 and bits[-2] == 'as':
                asvar = bits[-1]
                bits = bits[:-2]
            if len( bits ) >=1 and bits[-1] == 'with-inline':
                template = True
                bits = bits[:-1]
            elif len( bits ) >=2 and bits[-2] == 'with':
                template = bits[-1]
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
            if template == True:
                template = parser.parse(('end'+widget_name,))
                parser.delete_first_token()
            elif template:
                template = parser.compile_filter( template )
                
            return cls(args, kwargs, template, asvar)
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
        args = [arg.resolve( context ) for arg in self.args]
        kwargs = dict( [( smart_str( k, 'ascii' ), v.resolve( context ) ) for k, v in self.kwargs.items()] )
        
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
