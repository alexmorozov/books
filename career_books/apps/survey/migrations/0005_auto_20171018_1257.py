# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 09:57
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import survey.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20171018_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='title1',
            field=survey.models.BookForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title1', verbose_name=b'#1'),
        ),
        migrations.AlterField(
            model_name='result',
            name='title2',
            field=survey.models.BookForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title2', verbose_name=b'#2'),
        ),
        migrations.AlterField(
            model_name='result',
            name='title3',
            field=survey.models.BookForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title3', verbose_name=b'#3'),
        ),
    ]
