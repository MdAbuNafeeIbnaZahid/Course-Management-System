# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20170515_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='rank',
            field=models.CharField(blank=True, choices=[('PROFESSOR', 'Professor'), ('ASSOCIATE_PROF', 'Associate Professor'), ('ASSISTANT_PROF', 'Assistant Professor'), ('LECTURER', 'Lecturer')], max_length=200),
        ),
    ]
