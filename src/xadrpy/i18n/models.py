'''
Created on 2012.07.11.

@author: pcsaba
'''
from django.db import models
from xadrpy.models.inheritable import Inheritable

class TranslationForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("related_name", "+")
        self.language_code_field = kwargs.pop("language_code_field", "language_code")
        self.translator_name = kwargs.pop("translator", "trans")
        super(TranslationForeignKey, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        _self = self
        def trans(self, language_code):
            try:
                return cls.objects.get(**{name: self, _self.language_code_field:language_code})
            except:
                return self
        super(TranslationForeignKey, self).contribute_to_class(cls, name)
        cls._meta.unique_together = ((name, self.language_code_field),)
        setattr(self.rel.to, self.translator_name, trans)
    
class Translation(Inheritable):
    class Meta:
        abstract = True
