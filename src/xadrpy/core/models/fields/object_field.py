from copy import deepcopy
from base64 import b64encode, b64decode
from zlib import compress, decompress
try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

from django.db import models
from django.utils.encoding import force_unicode


class ObjectField( models.Field ):
    __metaclass__ = models.SubfieldBase

    class PickledObject( str ):
        pass


    def __init__( self, *args, **kwargs ):
        self.compress = kwargs.pop( 'compress', False )
        self.protocol = kwargs.pop( 'protocol', 2 )
        kwargs.setdefault( 'null', True )
        kwargs.setdefault( 'editable', False )
        super( ObjectField, self ).__init__( *args, **kwargs )

    def get_default( self ):
        if self.has_default():
            if callable( self.default ):
                return self.default()
            return self.default
        return super( ObjectField, self ).get_default()

    def to_python( self, value ):
        if value is not None:
            try:
                value = self._dbsafe_decode( value, self.compress )
            except:
                if isinstance( value, ObjectField.PickledObject ):
                    raise
        return value

    def get_db_prep_value( self, value, connection=None, prepared=False ):
        if value is not None and not isinstance( value, ObjectField.PickledObject ):
            value = force_unicode( self._dbsafe_encode( value, self.compress ) )
        return value

    def value_to_string( self, obj ):
        value = self._get_val_from_obj( obj )
        return self.get_db_prep_value( value )

    def get_internal_type( self ):
        return 'TextField'

    def get_db_prep_lookup( self, lookup_type, value, connection=None, prepared=False ):
        if lookup_type not in ['exact', 'in', 'isnull']:
            raise TypeError( 'Lookup type %s is not supported.' % lookup_type )
        return super( ObjectField, self ).get_db_prep_lookup( lookup_type, value )
    
    def _dbsafe_encode( self, value, compress_object = False ):
        if not compress_object:
            value = b64encode( dumps( deepcopy( value ) ) )
        else:
            value = b64encode( compress( dumps( deepcopy( value ) ) ) )
        return ObjectField.PickledObject( value )
    
    def _dbsafe_decode( self, value, compress_object = False ):
        if not compress_object:
            value = loads( b64decode( value ) )
        else:
            value = loads( decompress( b64decode( value ) ) )
        return value
    
try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.object_field\.ObjectField"])
