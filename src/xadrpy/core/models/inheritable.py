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
try:
    import mptt.managers
    import mptt.fields
    import mptt.models
    
    class TreeInheritableManager(mptt.managers.TreeManager):
        use_for_related_fields = True
        
        def get_query_set(self):
            return SubclassingQuerySet(self.model).order_by(self.tree_id_attr, self.left_attr)
    
    class TreeInheritable(mptt.models.MPTTModel):
    
        _default_manager = TreeInheritableManager()
        
        descendant_type = models.ForeignKey(ContentType, editable=False, related_name="+")
        descendant = GenericForeignKey(ct_field='descendant_type', fk_field='id')
        parent = mptt.fields.TreeForeignKey('self', null=True, blank=True, related_name='children')
    
        objects = TreeInheritableManager()
        tree = TreeInheritableManager()
    
        def get_root(self):
            return mptt.models.MPTTModel.get_root(self).descendant
    
        def get_parent(self):
            return self.parent and self.parent.descendant or None
    
        def save( self, *args, **kwargs ):
            if not self.pk:
                self.descendant_type = ContentType.objects.get_for_model( self )
            super( TreeInheritable, self ).save( *args, **kwargs )
    
        class Meta:
            abstract = True

except:
    pass