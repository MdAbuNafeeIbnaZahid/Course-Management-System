# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20170519_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum_post',
            name='document',
            field=models.FileField(null=True, upload_to='forum_post/'),
        ),
    ]
