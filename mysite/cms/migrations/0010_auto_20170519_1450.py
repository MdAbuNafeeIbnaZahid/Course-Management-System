# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 08:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20170519_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forum_post',
            old_name='clas_of_course',
            new_name='class_of_course',
        ),
    ]
