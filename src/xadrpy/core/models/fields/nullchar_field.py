from django.db import models

class NullCharField(models.CharField):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'null', True )
        kwargs.setdefault( 'blank', True )
        super( NullCharField, self ).__init__( *args, **kwargs )
    
    def get_prep_value(self, value):
        if not value and self.null:
            return None
        return self.to_python(value)

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.nullchar_field\.NullCharField"])
