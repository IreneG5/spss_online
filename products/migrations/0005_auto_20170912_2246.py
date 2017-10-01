# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20170830_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasetemp',
            name='product',
        ),
        migrations.RemoveField(
            model_name='purchasetemp',
            name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='productimage/'),
        ),
        migrations.DeleteModel(
            name='PurchaseTemp',
        ),
    ]
