# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 06:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0003_auto_20170428_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='inneruser',
            name='system_user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inneruser',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.Department'),
        ),
    ]
