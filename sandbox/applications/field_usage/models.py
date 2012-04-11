from django.db import models
from xadrpy.models.fields import PickledObjectField
from xadrpy.contrib.unique_id.fields import UniqueIdField

# Create your models here.
class TestModel(models.Model):
    name = models.CharField(max_length=200)
    data = PickledObjectField()
    basic_unique = UniqueIdField(prefix="TM", blank=True, null=True)