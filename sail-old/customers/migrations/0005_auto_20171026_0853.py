# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-26 00:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20171025_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transgoodsinfo',
            name='goods_key',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='customers.GoodsInfo'),
        ),
    ]
