# Generated by Django 2.2.4 on 2019-11-29 19:18

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_photo_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='hashtag',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
