from django.utils.translation import get_language
from django.conf import settings
from nullchar_field import NullCharField

class LanguageCodeField(NullCharField):
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'max_length', 5 )
        kwargs.setdefault( 'default', get_language )
        kwargs.setdefault( 'choices', settings.LANGUAGES )
        kwargs.setdefault( 'null', False )
        kwargs.setdefault( 'blank', False )
        kwargs.setdefault( 'db_index', True )
        super( LanguageCodeField, self ).__init__( *args, **kwargs )

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.language_code_field\.LanguageCodeField"])
    