# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-13 17:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.", regex='^\\d{10}')], verbose_name='phone_number'),
        ),
    ]
