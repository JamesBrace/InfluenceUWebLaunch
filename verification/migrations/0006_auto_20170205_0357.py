# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-05 03:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0005_auto_20170205_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='special_key',
            field=models.CharField(blank=True, default='123456', max_length=15),
        ),
    ]