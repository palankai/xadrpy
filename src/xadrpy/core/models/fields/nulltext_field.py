from django.db import models

class NullTextField(models.TextField):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'null', True )
        kwargs.setdefault( 'blank', True )
        super( NullTextField, self ).__init__( *args, **kwargs )
    
    def get_prep_value(self, value):
        if not value:
            return None
        return self.to_python(value)

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.nulltext_field\.NullTextField"])
