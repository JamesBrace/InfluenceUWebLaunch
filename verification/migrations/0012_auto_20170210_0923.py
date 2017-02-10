# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-10 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0011_auto_20170210_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineaccount',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='onlineaccount',
            name='shoe_size',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='storeaccount',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='storeaccount',
            name='shoe_size',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
