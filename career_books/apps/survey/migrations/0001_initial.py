# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import survey.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('li', '0007_auto_20170517_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('uid', models.CharField(default=survey.models.new_uid, editable=False, max_length=10, unique=True)),
                ('title1', models.CharField(default=b'', max_length=50, verbose_name=b'#1')),
                ('title2', models.CharField(default=b'', max_length=50, verbose_name=b'#2')),
                ('title3', models.CharField(default=b'', max_length=50, verbose_name=b'#3')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='li.Person')),
            ],
        ),
    ]
