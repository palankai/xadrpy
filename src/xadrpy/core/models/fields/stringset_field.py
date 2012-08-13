from django.db import models

__ALL__=['StringSetField', 'BigStringSetField']

class StringValue(unicode):
    pass

class BaseStringSetField(models.Field):

    def __init__( self, *args, **kwargs ):
        kwargs.setdefault('default', '')
        self.delimiter = kwargs.pop("delimiter", ",")
        self.lower = kwargs.pop("lower", False)
        self.upper = kwargs.pop("upper", False)
        self.enclosed = kwargs.pop("enclosed", True)
        super( BaseStringSetField, self ).__init__( *args, **kwargs )


    def to_python( self, value ):
        if isinstance( value, StringValue ):
            return value
        choices_values = self.get_choices_values()
        values = [self._trans(v).strip() for v in super(BaseStringSetField, self).to_python( value ).strip(self.delimiter).split(self.delimiter) if v.strip() and (not choices_values or v.strip() in choices_values)]
        return StringValue( self.delimiter.join(list(set(values))) )
    
    def _trans(self, value):
        if self.lower:
            value = value.lower()
        if self.upper:
            value = value.upper()
        return value

    def get_db_prep_value( self, value, connection=None, prepared=False ):
        if value is not None \
            and not isinstance( value, StringValue ):
                raise ValueError()
        value = value.strip(self.delimiter)
        if self.enclosed and value:
            value = self.delimiter+value+self.delimiter
        return super(BaseStringSetField, self).get_db_prep_value( value, connection, prepared )

    def get_choices_values(self):
        if not self.choices:
            return None
        return dict(self.choices).keys()

class StringSetField(BaseStringSetField):
    __metaclass__ = models.SubfieldBase

    def __init__( self, *args, **kwargs ):
        kwargs.setdefault('max_length', 255)
        super( StringSetField, self ).__init__( *args, **kwargs )

    def get_internal_type(self):
        return 'CharField'

class BigStringSetField(BaseStringSetField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'TextField'

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.stringset_field\.StringSetField"])
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.stringset_field\.BigStringSetField"])
