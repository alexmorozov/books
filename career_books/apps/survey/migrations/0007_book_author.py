# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20171019_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
    ]
