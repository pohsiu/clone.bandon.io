# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-03 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandongo', '0016_auto_20170203_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='finish',
            field=models.BooleanField(default=False),
        ),
    ]
