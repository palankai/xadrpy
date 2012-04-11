# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TestModel.basic_unique'
        db.add_column('field_usage_testmodel', 'basic_unique',
                      self.gf('xadrpy.contrib.unique_id.fields.UniqueIdField')(max_length=255, unique=True, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'TestModel.basic_unique'
        db.delete_column('field_usage_testmodel', 'basic_unique')

    models = {
        'field_usage.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'basic_unique': ('xadrpy.contrib.unique_id.fields.UniqueIdField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'data': ('xadrpy.models.fields.pickled_object_field.PickledObjectField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['field_usage']