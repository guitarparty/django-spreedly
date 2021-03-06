# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Plan'
        db.create_table('spreedly_plan', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('terms', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('plan_type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=8, decimal_places=2)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('force_recurring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('force_renew', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('duration_units', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('feature_level', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('return_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('speedly_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_index=True)),
            ('speedly_site_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('spreedly', ['Plan'])

        # Adding model 'Subscription'
        db.create_table('spreedly_subscription', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('feature_level', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('active_until', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('trial_elegible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lifetime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recurring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('card_expires_before_next_auto_renew', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('store_credit', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('spreedly', ['Subscription'])

        # Adding model 'Gift'
        db.create_table('spreedly_gift', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, db_index=True)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gifts_sent', to=orm['auth.User'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gifts_received', to=orm['auth.User'])),
            ('plan_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('sent_at', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('spreedly', ['Gift'])


    def backwards(self, orm):
        
        # Deleting model 'Plan'
        db.delete_table('spreedly_plan')

        # Deleting model 'Subscription'
        db.delete_table('spreedly_subscription')

        # Deleting model 'Gift'
        db.delete_table('spreedly_gift')


    models = {
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 22, 14, 53, 37, 780358)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 22, 14, 53, 37, 780259)'}),
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
        },
        'spreedly.gift': {
            'Meta': {'object_name': 'Gift'},
            'created_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gifts_sent'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'plan_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sent_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gifts_received'", 'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        'spreedly.plan': {
            'Meta': {'ordering': "['order', 'price']", 'object_name': 'Plan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'duration_units': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feature_level': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'force_recurring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'force_renew': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'plan_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'return_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speedly_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_index': 'True'}),
            'speedly_site_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'terms': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'spreedly.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'active_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'card_expires_before_next_auto_renew': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feature_level': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lifetime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recurring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'store_credit': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'trial_elegible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['spreedly']
