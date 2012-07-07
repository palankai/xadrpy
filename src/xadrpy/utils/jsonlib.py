import datetime
import decimal
from xadrpy.utils.primitives import PrettyFloat, Native
from simplejson.encoder import encode_basestring_ascii, encode_basestring
import simplejson as json

class JSONEncoder( json.JSONEncoder ):
    
    def default( self, obj ):
        if isinstance( obj, datetime.datetime ):                                                                                                                                                                                                                                 
            return obj.strftime( '%Y-%m-%d %H:%M:%S' )                                                                                                                                                                                                                           
        if isinstance( obj, datetime.date ):                                                                                                                                                                                                                                   
            return obj.strftime( '%Y-%m-%d' )                                                                                                                                                                                                                                    
        if isinstance( obj, datetime.time ):                                                                                                                                                                                                                                   
            return obj.strftime( '%H:%M:%S' )
        if isinstance( obj, datetime.timedelta ):
            if obj.microseconds:                                                                                                                                                                                                                                   
                return PrettyFloat((float(obj.microseconds) + (obj.seconds + obj.days * 24 * 3600) * 10**6) / 10**6) 
            else:
                return (obj.seconds + obj.days * 24 * 3600)
        try:
            return json.JSONEncoder.default( self, obj )
        except TypeError:
            return self._object_serializer(obj)

    def _object_serializer(self,obj):
        import types
        result = {}
        classes = [cls for cls in obj.__class__.__bases__]
        classes.append(obj.__class__)
        for cls in classes:
            for i in cls.__dict__:
                if not i.startswith("_"):
                    value = getattr(obj, i)
                    if not isinstance(value, types.MethodType):
                        result[i]=value
        result.update(obj.__dict__)
        return result
