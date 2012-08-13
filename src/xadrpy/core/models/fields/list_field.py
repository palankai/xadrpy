from object_field import ObjectField
from django.db import models
from xadrpy.utils.jsonlib import JSONEncoder

class ListField(ObjectField):
    __metaclass__ = models.SubfieldBase
    
    class ListFieldValue( list ):
        def to_json(self):
            return JSONEncoder().encode(self)

    def __init__( self, *args, **kwargs ):
        kwargs['blank'] = False
        kwargs['null'] = False
        
        kwargs.setdefault( 'null', False )
        kwargs.setdefault( 'default', [] )
        super( ListField, self ).__init__( *args, **kwargs )
    
    def to_python( self, value ):
        if isinstance( value, ListField.ListFieldValue ):
            return value
        if isinstance( value, list ):
            return ListField.ListFieldValue(value)
        return ListField.ListFieldValue( super(ListField, self).to_python( value ) )

    def get_db_prep_value( self, value, connection=None, prepared=False ):
        if value is not None \
            and not isinstance( value, ObjectField.PickledObject ) \
            and not isinstance( value, list):
                raise ValueError()
        return super(ListField, self).get_db_prep_value( value, connection, prepared )

    def _dbsafe_encode( self, value, compress_object = False ):
        return super(ListField, self)._dbsafe_encode( list(value), compress_object )


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.list_field\.ListField"])
