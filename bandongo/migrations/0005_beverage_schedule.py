# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-17 17:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bandongo', '0004_auto_20170117_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('pic', models.URLField(blank=True)),
                ('telepone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('remark', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('beverage', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bandongo.Beverage')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandongo.Shop')),
            ],
        ),
    ]
