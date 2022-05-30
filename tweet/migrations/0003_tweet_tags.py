# Generated by Django 4.0.4 on 2022-05-30 08:08

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('tweet', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
