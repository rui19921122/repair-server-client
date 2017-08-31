# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-15 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MockPlanHistoryList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.PositiveSmallIntegerField(choices=[(0, '第一天'), (1, '第二天'), (2, '第三天')])),
                ('plan_type', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('plan_time', models.CharField(max_length=100)),
                ('repair_content', models.CharField(max_length=100)),
                ('repair_department', models.CharField(max_length=100)),
                ('apply_place', models.CharField(max_length=100)),
                ('inner_id', models.CharField(max_length=100)),
                ('use_paper', models.BooleanField(default=False)),
            ],
        ),
    ]