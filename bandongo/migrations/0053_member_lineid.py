# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-16 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandongo', '0052_auto_20170316_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='lineId',
            field=models.CharField(default='', max_length=100),
        ),
    ]
