# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=128, verbose_name='\u5bc6\u7801'),
        ),
    ]