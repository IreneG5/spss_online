# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_auto_20170926_0028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='product_rel',
            new_name='product',
        ),
    ]