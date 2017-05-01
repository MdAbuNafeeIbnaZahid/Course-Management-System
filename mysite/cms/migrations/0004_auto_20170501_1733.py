# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20170501_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='rank',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='department',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='division',
            field=models.CharField(blank=True, choices=[('BARISHAL', 'Barishal'), ('CHITTAGONG', 'Chittagong'), ('DHAKA', 'Dhaka'), ('MYMENSINGH', 'Mymensingh'), ('KHULNA', 'Khulna'), ('RAJSHAHI', 'Rajshahi'), ('RANGPUR', 'Rangpur'), ('SYLHET', 'Sylhet')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_nom',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='joinDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_nom',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]