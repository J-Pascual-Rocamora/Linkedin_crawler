# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-29 00:27
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_data', '0002_auto_20171029_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalemployee',
            name='ai_endorsements',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]