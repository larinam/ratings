# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('ratings4you_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('authorization_mode', self.gf('django.db.models.fields.CharField')(default='Authorized', max_length=255)),
            ('bonus_currency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('profile_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('ratings4you', ['UserProfile'])

        # Adding model 'RatingThemesDirectory'
        db.create_table('ratings4you_ratingthemesdirectory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.RatingThemesDirectory'], null=True)),
        ))
        db.send_create_signal('ratings4you', ['RatingThemesDirectory'])

        # Adding model 'RegionDirectory'
        db.create_table('ratings4you_regiondirectory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.RegionDirectory'], null=True)),
        ))
        db.send_create_signal('ratings4you', ['RegionDirectory'])

        # Adding model 'Rating'
        db.create_table('ratings4you_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.RegionDirectory'])),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.RatingThemesDirectory'])),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 11, 16, 12, 34, 45, 758189), auto_now=True, blank=True)),
            ('time_moderated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('ratings4you', ['Rating'])

        # Adding model 'RatingItem'
        db.create_table('ratings4you_ratingitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.Rating'])),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 11, 16, 12, 34, 45, 759097), auto_now=True, blank=True)),
            ('time_moderated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('ratings4you', ['RatingItem'])

        # Adding model 'Vote'
        db.create_table('ratings4you_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vote_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('rating_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings4you.RatingItem'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('ratings4you', ['Vote'])

        # Adding model 'KVTable'
        db.create_table('ratings4you_kvtable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key_column', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value_column', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ratings4you', ['KVTable'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('ratings4you_userprofile')

        # Deleting model 'RatingThemesDirectory'
        db.delete_table('ratings4you_ratingthemesdirectory')

        # Deleting model 'RegionDirectory'
        db.delete_table('ratings4you_regiondirectory')

        # Deleting model 'Rating'
        db.delete_table('ratings4you_rating')

        # Deleting model 'RatingItem'
        db.delete_table('ratings4you_ratingitem')

        # Deleting model 'Vote'
        db.delete_table('ratings4you_vote')

        # Deleting model 'KVTable'
        db.delete_table('ratings4you_kvtable')


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
        },
        'ratings4you.kvtable': {
            'Meta': {'object_name': 'KVTable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_column': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value_column': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ratings4you.rating': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Rating'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 11, 16, 12, 34, 45, 758189)', 'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.RegionDirectory']"}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.RatingThemesDirectory']"}),
            'time_moderated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'ratings4you.ratingitem': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RatingItem'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 11, 16, 12, 34, 45, 759097)', 'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.Rating']"}),
            'time_moderated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'ratings4you.ratingthemesdirectory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RatingThemesDirectory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.RatingThemesDirectory']", 'null': 'True'})
        },
        'ratings4you.regiondirectory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RegionDirectory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.RegionDirectory']", 'null': 'True'})
        },
        'ratings4you.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'authorization_mode': ('django.db.models.fields.CharField', [], {'default': "'Authorized'", 'max_length': '255'}),
            'bonus_currency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'ratings4you.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'rating_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings4you.RatingItem']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ratings4you']
