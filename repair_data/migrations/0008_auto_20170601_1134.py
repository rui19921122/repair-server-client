# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-01 03:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_data', '0007_auto_20170601_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detaildata',
            name='actual_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='actual_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='plan_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='plan_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
