from xadrpy.core.models.inheritable import Inheritable
from django.utils.translation import get_language
    
class Translation(Inheritable):
    
    @classmethod
    def register(cls, origin_cls):
        field = origin_cls._translation_foreign_key_field
        
        def trans(self, language_code=None, get_or_create=False):
            if not language_code:
                language_code = get_language()
            try:
                kwargs = {field.name: self, field.language_code_field:language_code}
                if get_or_create:
                    try:
                        obj = cls.objects.get(**kwargs)
                    except:
                        obj = cls(**kwargs)
                        obj.set_defaults(getattr(obj, field.name))
                        obj.save()
                else:
                    obj = cls.objects.get(**kwargs)
                return getattr(obj, 'descendant', obj) 
            except cls.DoesNotExist:
                return self
        setattr(origin_cls, field.translator_name, trans)
    
    def set_defaults(self, origin):
        pass
    
    class Meta:
        abstract = True
