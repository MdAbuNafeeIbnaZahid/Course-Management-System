# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 06:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20170501_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option_of_vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question_of_vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('respodent_type', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response_of_vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Option_of_vote')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Question_of_vote')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='option_of_vote',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Question_of_vote'),
        ),
        migrations.AlterUniqueTogether(
            name='response_of_vote',
            unique_together=set([('question', 'teacher', 'student')]),
        ),
    ]