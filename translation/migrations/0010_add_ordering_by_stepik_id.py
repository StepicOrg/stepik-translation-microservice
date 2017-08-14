# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0009_change_course_on_delete_to_null'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translatedcourse',
            options={'ordering': ['stepik_id']},
        ),
        migrations.AlterModelOptions(
            name='translatedlesson',
            options={'ordering': ['stepik_id']},
        ),
        migrations.AlterField(
            model_name='translatedlesson',
            name='stepik_id',
            field=models.IntegerField(),
        ),
    ]
