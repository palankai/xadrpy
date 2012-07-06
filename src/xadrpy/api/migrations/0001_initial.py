# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('xadrpy_api_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('static_key', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, unique=True, null=True, blank=True)),
            ('client_id', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, unique=True, null=True, blank=True)),
            ('client_secret', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('client_type', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('scope', self.gf('xadrpy.models.fields.json_field.JSONField')(default=[], null=True, blank=True)),
            ('data', self.gf('xadrpy.models.fields.json_field.JSONField')(default={}, null=True, blank=True)),
            ('redirect_uri', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('api', ['Client'])

        # Adding model 'Access'
        db.create_table('xadrpy_api_access', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('scope', self.gf('xadrpy.models.fields.json_field.JSONField')(default=[], null=True, blank=True)),
            ('data', self.gf('xadrpy.models.fields.json_field.JSONField')(default={}, null=True, blank=True)),
        ))
        db.send_create_signal('api', ['Access'])

        # Adding unique constraint on 'Access', fields ['user', 'client']
        db.create_unique('xadrpy_api_access', ['user_id', 'client_id'])

        # Adding model 'Token'
        db.create_table('xadrpy_api_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('expired', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('timeout', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('data', self.gf('xadrpy.models.fields.json_field.JSONField')(default={}, null=True, blank=True)),
        ))
        db.send_create_signal('api', ['Token'])


    def backwards(self, orm):
        # Removing unique constraint on 'Access', fields ['user', 'client']
        db.delete_unique('xadrpy_api_access', ['user_id', 'client_id'])

        # Deleting model 'Client'
        db.delete_table('xadrpy_api_client')

        # Deleting model 'Access'
        db.delete_table('xadrpy_api_access')

        # Deleting model 'Token'
        db.delete_table('xadrpy_api_token')


    models = {
        'api.access': {
            'Meta': {'unique_together': "(('user', 'client'),)", 'object_name': 'Access', 'db_table': "'xadrpy_api_access'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('xadrpy.models.fields.json_field.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'scope': ('xadrpy.models.fields.json_field.JSONField', [], {'default': '[]', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.client': {
            'Meta': {'object_name': 'Client', 'db_table': "'xadrpy_api_client'"},
            'client_id': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'client_secret': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_type': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('xadrpy.models.fields.json_field.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'redirect_uri': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scope': ('xadrpy.models.fields.json_field.JSONField', [], {'default': '[]', 'null': 'True', 'blank': 'True'}),
            'static_key': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'api.token': {
            'Meta': {'object_name': 'Token', 'db_table': "'xadrpy_api_token'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('xadrpy.models.fields.json_field.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'expired': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']