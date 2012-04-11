from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.descendant
        else :
            return result
        
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.descendant


class InheritableManager(models.Manager):
    use_for_related_fields = True
    
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class Inheritable(models.Model):
    descendant_type = models.ForeignKey(ContentType, editable=False, related_name="+")
    descendant = GenericForeignKey(ct_field='descendant_type', fk_field='id')

    def save( self, *args, **kwargs ):
        if not self.pk:
            self.descendant_type = ContentType.objects.get_for_model( self )
        super( Inheritable, self ).save( *args, **kwargs )
    
    objects = InheritableManager()
        
    class Meta:
        abstract = True
