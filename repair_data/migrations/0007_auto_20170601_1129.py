# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-01 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_data', '0006_auto_20170601_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detaildata',
            name='repair_check_in_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
