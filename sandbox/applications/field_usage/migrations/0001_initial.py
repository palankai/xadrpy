# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestModel'
        db.create_table('field_usage_testmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('data', self.gf('xadrpy.models.fields.pickled_object_field.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('field_usage', ['TestModel'])

    def backwards(self, orm):
        # Deleting model 'TestModel'
        db.delete_table('field_usage_testmodel')

    models = {
        'field_usage.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'data': ('xadrpy.models.fields.pickled_object_field.PickledObjectField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['field_usage']