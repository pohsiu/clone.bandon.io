# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-22 22:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandongo', '0046_auto_20170220_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='choosed',
        ),
        migrations.AddField(
            model_name='schedule',
            name='catalogs',
            field=models.ManyToManyField(to='bandongo.Catalog'),
        ),
    ]