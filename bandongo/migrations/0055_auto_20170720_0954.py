# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-20 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bandongo', '0054_auto_20170616_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savelog',
            name='adminName',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin', to='bandongo.Member'),
        ),
    ]
