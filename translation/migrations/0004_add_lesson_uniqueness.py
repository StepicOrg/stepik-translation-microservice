# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0003_rename_date_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translatedlesson',
            name='stepik_id',
            field=models.IntegerField(unique=True),
        ),
    ]
