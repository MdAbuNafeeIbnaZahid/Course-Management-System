# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 02:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone_nom', models.IntegerField(null=True)),
                ('email_address', models.EmailField(max_length=254, null=True)),
                ('joinDate', models.DateField(null=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Teacher'),
        ),
    ]
