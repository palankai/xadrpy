from django.db import models
from xadrpy.core.models.fields.class_field import ClassNameField
import base
from xadrpy.core.preferences.fields import PrefsStoreField
from xadrpy.core.models.fields.json_field import JSONField

class InstalledTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    config = JSONField()
    handler_name = ClassNameField('theme', ifnull=base.Theme)
    prefs_store = PrefsStoreField('prefs')