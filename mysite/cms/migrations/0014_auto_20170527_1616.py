# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 10:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20170526_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(null=True, upload_to='submission/')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Submission_window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=999, validators=[django.core.validators.MinLengthValidator(1)])),
                ('body', models.TextField(max_length=9999, validators=[django.core.validators.MinLengthValidator(1)])),
                ('end_time', models.DateTimeField()),
                ('class_of_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Class_of_course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Submission_window'),
        ),
    ]
