from django.db import models
from models import UniqueId
import conf

class UniqueIdField( models.Field ):
    __metaclass__ = models.SubfieldBase

    def __init__( self, *args, **kwargs ):
        self._length = kwargs.pop('length',conf.UNIQUE_ID_DEFAULT_LENGTH)
        self._chars = kwargs.pop('chars',conf.UNIQUE_ID_DEFAULT_CHARS)
        self._prefix = kwargs.pop('prefix', None)
        self._suffix = kwargs.pop('suffix', None)
        assert kwargs.pop("default", None) == None
        options = {
           'blank': False, 
           'null': False,
           'editable': False,
           'unique': True,
           'max_length': 255,
        }
        options.update(kwargs)
        super( UniqueIdField, self ).__init__( *args, **options )

    def get_default( self ):
        return UniqueId.objects.get_unique_id(length=self._length, chars=self._chars, prefix=self._prefix, suffix=self._suffix).get_id()

    def get_internal_type( self ):
        return 'CharField'
    

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.contrib\.unique_id\.fields\.UniqueIdField"])
