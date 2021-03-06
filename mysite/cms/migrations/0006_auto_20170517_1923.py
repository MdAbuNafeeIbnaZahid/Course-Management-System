# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20170517_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolment',
            name='approval_status',
            field=models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('WAITING_FOR_APPROVAL', 'Waiting for approval')], default='WAITING_FOR_APPROVAL', max_length=200),
        ),
    ]
