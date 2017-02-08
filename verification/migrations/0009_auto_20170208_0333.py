# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-08 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0008_auto_20170207_0727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.AddField(
            model_name='account',
            name='buying_option',
            field=models.CharField(blank=True, default='Store', max_length=40),
        ),
        migrations.AddField(
            model_name='account',
            name='full_name',
            field=models.CharField(default='Fake Name', max_length=40),
        ),
        migrations.AddField(
            model_name='account',
            name='shoe_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='account',
            name='has_submitted_shoe',
            field=models.BooleanField(default=True),
        ),
    ]
