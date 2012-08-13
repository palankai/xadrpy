from object_field import ObjectField
from django.db import models
from xadrpy.utils.jsonlib import JSONEncoder


class DictField(ObjectField):
    __metaclass__ = models.SubfieldBase
    
    class DictFieldValue( dict ):
        def to_json(self):
            return JSONEncoder().encode(self)

    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'null', False )
        kwargs.setdefault( 'default', {} )
        super( DictField, self ).__init__( *args, **kwargs )
    
    def to_python( self, value ):
        if isinstance( value, DictField.DictFieldValue ):
            return value
        return DictField.DictFieldValue( super(DictField, self).to_python( value ) )

    def get_db_prep_value( self, value, connection=None, prepared=False ):
        if value is not None \
            and not isinstance( value, ObjectField.PickledObject ) \
            and not isinstance( value, dict):
                raise ValueError()
        return super(DictField, self).get_db_prep_value( value, connection, prepared )

    def _dbsafe_encode( self, value, compress_object = False ):
        return super(DictField, self)._dbsafe_encode( dict(value), compress_object )


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.core\.models\.fields\.dict_field\.DictField"])
