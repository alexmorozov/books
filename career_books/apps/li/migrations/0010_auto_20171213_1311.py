# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('li', '0009_person_connected_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_type',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='company',
            name='employee_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='company',
            name='year_founded',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
