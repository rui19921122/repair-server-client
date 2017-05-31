# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-31 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repair_check_in_method', models.CharField(max_length=50)),
                ('plan_id', models.CharField(max_length=50)),
                ('plan_work_during', models.CharField(max_length=50)),
                ('is_ok', models.CharField(max_length=50)),
                ('actual_start_time', models.CharField(max_length=50)),
                ('repair_type', models.CharField(max_length=50)),
                ('actual_start_number', models.CharField(max_length=50)),
                ('inner_id', models.CharField(max_length=50)),
                ('actual_end_time', models.CharField(max_length=50)),
                ('plan_start_time', models.CharField(max_length=50)),
                ('actual_person', models.CharField(max_length=50)),
                ('repair_check_in_area', models.CharField(max_length=50)),
                ('repair_area', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('actual_work_during', models.CharField(max_length=50)),
                ('repair_unit', models.CharField(max_length=50)),
                ('actual_end_number', models.CharField(max_length=50)),
                ('plan_end_time', models.CharField(max_length=50)),
            ],
        ),
    ]