# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-15 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_data', '0002_mockplanhistorydetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockplanhistorydetail',
            name='inner_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
