# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_merge_20171020_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='is_invited',
            field=models.DateTimeField(null=True),
        ),
    ]
