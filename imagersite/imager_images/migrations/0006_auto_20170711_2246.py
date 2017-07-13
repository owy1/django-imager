# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0005_auto_20170711_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='published',
            field=models.CharField(choices=[('PB', 'public'), ('PV', 'private'), ('SH', 'shared')], default='PB', max_length=2),
        ),
    ]
