# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='level_name',
            field=models.CharField(default='Newbie', max_length=15),
        ),
    ]