# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20170918_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='products.Purchase'),
        ),
    ]
