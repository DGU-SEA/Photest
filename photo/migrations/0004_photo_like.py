# Generated by Django 2.2.4 on 2019-11-29 19:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photo', '0003_auto_20191129_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
