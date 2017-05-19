# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20170518_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=9999)),
                ('clas_of_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Class_of_course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Teacher')),
            ],
        ),
    ]
