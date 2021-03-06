# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-01 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_data', '0004_auto_20170531_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detaildata',
            name='actual_person',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='actual_start_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='inner_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='repair_area',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='repair_check_in_area',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='repair_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detaildata',
            name='repair_unit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
