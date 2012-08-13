from django.utils import simplejson
from django.db import models
from xadrpy.utils.jsonlib import JSONEncoder
from django.utils.encoding import force_unicode

class JSONField(models.Field):

    __metaclass__ = models.SubfieldBase

    class EncodedJSONObject( str ):
        pass
    
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['unique'] = False
        kwargs['db_index'] = False
        kwargs.setdefault('editable', False)
        super(JSONField, self).__init__(*args, **kwargs)
        
    def get_default( self ):
        if self.has_default():
            if callable( self.default ):
                return self.default()
            return self.default
        return super( JSONField, self ).get_default()

    def to_python(self, value):

        if value is not None:
            try:
                value = self._dbsafe_decode( value )
            except:
                if isinstance( value, JSONField.EncodedJSONObject ):
                    raise
        return value        

    def get_prep_value(self, value, connection=None, prepared=False):
        if value is not None and not isinstance( value, JSONField.EncodedJSONObject ):
            value = force_unicode( self._dbsafe_encode( value ) )
        return value
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)    
    
    def get_internal_type(self):
        return 'TextField'

    def get_db_prep_lookup( self, lookup_type, value, connection=None, prepared=False ):
        if lookup_type not in ['isnull']:
            raise TypeError( 'Lookup type %s is not supported.' % lookup_type )
        return super( JSONField, self ).get_db_prep_lookup( lookup_type, value )    

    def _dbsafe_encode( self, value ):
        value = JSONEncoder().encode(value)
        return JSONField.EncodedJSONObject( value )
    
    def _dbsafe_decode( self, value ):
        value = simplejson.loads( value )
        return value


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.json_field\.JSONField"])
