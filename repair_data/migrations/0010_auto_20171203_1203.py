# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-03 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_data', '0009_auto_20171130_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detaildata',
            name='repair_type',
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='actual_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='actual_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='plan_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='plan_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
