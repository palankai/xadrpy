from django.db import models

class KeyTableField(models.ForeignKey): 
    def __init__(self, key_table_name, **kwargs):
        limit_choices_to = kwargs.pop("limit_choices_to", {})
        limit_choices_to.update({
            'key_table__name': key_table_name,
        })
        kwargs.update({
            'related_name': "+"
        })
        super(KeyTableField, self).__init__("dynamic.KeyTableEntry", limit_choices_to=limit_choices_to, **kwargs)

class MultiKeyTableField(models.ManyToManyField):
    def __init__(self, key_table_name, **kwargs):
        limit_choices_to = kwargs.pop("limit_choices_to", {})
        limit_choices_to.update({
            'key_table__name': key_table_name,
        })
        kwargs['related_name']="%s_%s+" % (key_table_name, self.creation_counter)
        super(MultiKeyTableField, self).__init__("dynamic.KeyTableEntry", limit_choices_to=limit_choices_to, **kwargs)

class AttributeForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("related_name", "dynamic_attributes")
        super(AttributeForeignKey, self).__init__(*args, **kwargs)
    
    def contribute_to_related_class(self, cls, related):
        models.ForeignKey.contribute_to_related_class(self, cls, related)
        setattr(related, "_attribute_foreign_key_field", self)

    def contribute_to_class(self, cls, name):
        super(AttributeForeignKey, self).contribute_to_class(cls, name)
        cls._meta.unique_together = ((name, "attribute_type", "language_code"),)
        if not isinstance(self.rel.to, basestring):
            setattr(self.rel.to, "_attribute_foreign_key_field", self)
            

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^xadrpy\.contrib\.dynamic\.fields\.AttributeForeignKey"])
    add_introspection_rules([], [r"^xadrpy\.contrib\.dynamic\.fields\.KeyTableField"])
    add_introspection_rules([], [r"^xadrpy\.contrib\.dynamic\.fields\.MultiKeyTableField"])


