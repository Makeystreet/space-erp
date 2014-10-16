# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Space'
        db.create_table(u'erp_space', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.URLField')(max_length=400, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=15, decimal_places=10, blank=True)),
            ('map_zoom_level', self.gf('django.db.models.fields.IntegerField')(default=13)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('no_of_members', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('membership_fee', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('date_of_founding', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_updated_external', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('erp', ['Space'])

        # Adding M2M table for field admins on 'Space'
        m2m_table_name = db.shorten_name(u'erp_space_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['erp.space'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'user_id'])

        # Adding M2M table for field members on 'Space'
        m2m_table_name = db.shorten_name(u'erp_space_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['erp.space'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'user_id'])

        # Adding model 'Part'
        db.create_table(u'erp_part', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('erp', ['Part'])

        # Adding model 'Inventory'
        db.create_table(u'erp_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_part', to=orm['erp.Part'])),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_space', to=orm['erp.Space'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('erp', ['Inventory'])


    def backwards(self, orm):
        # Deleting model 'Space'
        db.delete_table(u'erp_space')

        # Removing M2M table for field admins on 'Space'
        db.delete_table(db.shorten_name(u'erp_space_admins'))

        # Removing M2M table for field members on 'Space'
        db.delete_table(db.shorten_name(u'erp_space_members'))

        # Deleting model 'Part'
        db.delete_table(u'erp_part')

        # Deleting model 'Inventory'
        db.delete_table(u'erp_inventory')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'erp.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_part'", 'to': "orm['erp.Part']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_space'", 'to': "orm['erp.Space']"})
        },
        'erp.part': {
            'Meta': {'object_name': 'Part'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'erp.space': {
            'Meta': {'object_name': 'Space'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'space_admins'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_of_founding': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'space_inventory'", 'symmetrical': 'False', 'through': "orm['erp.Inventory']", 'to': "orm['erp.Part']"}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'last_updated_external': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'map_zoom_level': ('django.db.models.fields.IntegerField', [], {'default': '13'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'space_members'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'membership_fee': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'no_of_members': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['erp']