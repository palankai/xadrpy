# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table('xadrpy_router_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descendant_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['router.Route'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['router.Route'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('language_code', self.gf('xadrpy.models.fields.language_code_field.LanguageCodeField')(default=None, max_length=5, null=True, db_index=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('i18n', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('signature', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(default='', max_length=128, null=True, blank=True)),
            ('meta', self.gf('xadrpy.models.fields.dict_field.DictField')(default={})),
            ('meta_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('overwrite_meta_title', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('router', ['Route'])

        # Adding unique constraint on 'Route', fields ['site', 'language_code', 'parent', 'slug']
        db.create_unique('xadrpy_router_route', ['site_id', 'language_code', 'parent_id', 'slug'])

        # Adding model 'RouteTranslation'
        db.create_table('xadrpy_router_route_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descendant_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('origin', self.gf('xadrpy.i18n.fields.TranslationForeignKey')(related_name='+', to=orm['router.Route'])),
            ('language_code', self.gf('xadrpy.models.fields.language_code_field.LanguageCodeField')(default='en-us', max_length=5, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('meta', self.gf('xadrpy.models.fields.dict_field.DictField')(default={})),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('router', ['RouteTranslation'])

        # Adding unique constraint on 'RouteTranslation', fields ['origin', 'language_code']
        db.create_unique('xadrpy_router_route_translation', ['origin_id', 'language_code'])

        # Adding model 'ViewRoute'
        db.create_table('xadrpy_router_view', (
            ('route_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['router.Route'], unique=True, primary_key=True)),
            ('view_name', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('router', ['ViewRoute'])

        # Adding model 'IncludeRoute'
        db.create_table('xadrpy_router_include', (
            ('route_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['router.Route'], unique=True, primary_key=True)),
            ('include_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('namespace', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
            ('app_name', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('router', ['IncludeRoute'])

        # Adding model 'StaticRoute'
        db.create_table('xadrpy_router_static', (
            ('route_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['router.Route'], unique=True, primary_key=True)),
            ('path', self.gf('django.db.models.fields.FilePathField')(max_length=255)),
            ('mimetype', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('router', ['StaticRoute'])

        # Adding model 'TemplateRoute'
        db.create_table('xadrpy_router_template', (
            ('route_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['router.Route'], unique=True, primary_key=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mimetype', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('router', ['TemplateRoute'])

        # Adding model 'RedirectRoute'
        db.create_table('xadrpy_router_redirect', (
            ('route_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['router.Route'], unique=True, primary_key=True)),
            ('url', self.gf('xadrpy.models.fields.nullchar_field.NullCharField')(max_length=255)),
            ('permanent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('router', ['RedirectRoute'])


    def backwards(self, orm):
        # Removing unique constraint on 'RouteTranslation', fields ['origin', 'language_code']
        db.delete_unique('xadrpy_router_route_translation', ['origin_id', 'language_code'])

        # Removing unique constraint on 'Route', fields ['site', 'language_code', 'parent', 'slug']
        db.delete_unique('xadrpy_router_route', ['site_id', 'language_code', 'parent_id', 'slug'])

        # Deleting model 'Route'
        db.delete_table('xadrpy_router_route')

        # Deleting model 'RouteTranslation'
        db.delete_table('xadrpy_router_route_translation')

        # Deleting model 'ViewRoute'
        db.delete_table('xadrpy_router_view')

        # Deleting model 'IncludeRoute'
        db.delete_table('xadrpy_router_include')

        # Deleting model 'StaticRoute'
        db.delete_table('xadrpy_router_static')

        # Deleting model 'TemplateRoute'
        db.delete_table('xadrpy_router_template')

        # Deleting model 'RedirectRoute'
        db.delete_table('xadrpy_router_redirect')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'router.includeroute': {
            'Meta': {'object_name': 'IncludeRoute', 'db_table': "'xadrpy_router_include'", '_ormbases': ['router.Route']},
            'app_name': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'include_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'namespace': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'route_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['router.Route']", 'unique': 'True', 'primary_key': 'True'})
        },
        'router.redirectroute': {
            'Meta': {'object_name': 'RedirectRoute', 'db_table': "'xadrpy_router_redirect'", '_ormbases': ['router.Route']},
            'permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'route_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['router.Route']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255'})
        },
        'router.route': {
            'Meta': {'unique_together': "(('site', 'language_code', 'parent', 'slug'),)", 'object_name': 'Route', 'db_table': "'xadrpy_router_route'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descendant_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'i18n': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language_code': ('xadrpy.models.fields.language_code_field.LanguageCodeField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['router.Route']"}),
            'meta': ('xadrpy.models.fields.dict_field.DictField', [], {'default': '{}'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'overwrite_meta_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['router.Route']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'signature': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'slug': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'router.routetranslation': {
            'Meta': {'unique_together': "(('origin', 'language_code'),)", 'object_name': 'RouteTranslation', 'db_table': "'xadrpy_router_route_translation'"},
            'descendant_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language_code': ('xadrpy.models.fields.language_code_field.LanguageCodeField', [], {'default': "'en-us'", 'max_length': '5', 'db_index': 'True'}),
            'meta': ('xadrpy.models.fields.dict_field.DictField', [], {'default': '{}'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'origin': ('xadrpy.i18n.fields.TranslationForeignKey', [], {'related_name': "'+'", 'to': "orm['router.Route']"}),
            'slug': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'router.staticroute': {
            'Meta': {'object_name': 'StaticRoute', 'db_table': "'xadrpy_router_static'", '_ormbases': ['router.Route']},
            'mimetype': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [], {'max_length': '255'}),
            'route_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['router.Route']", 'unique': 'True', 'primary_key': 'True'})
        },
        'router.templateroute': {
            'Meta': {'object_name': 'TemplateRoute', 'db_table': "'xadrpy_router_template'", '_ormbases': ['router.Route']},
            'mimetype': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'route_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['router.Route']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'router.viewroute': {
            'Meta': {'object_name': 'ViewRoute', 'db_table': "'xadrpy_router_view'", '_ormbases': ['router.Route']},
            'name': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'route_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['router.Route']", 'unique': 'True', 'primary_key': 'True'}),
            'view_name': ('xadrpy.models.fields.nullchar_field.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['router']