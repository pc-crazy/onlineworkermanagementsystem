# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-15 04:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worker', '0003_auto_20180413_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_otp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='workerprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_worker_profile', related_query_name='<QuerySet [<User: 9999999999>, <User: 9797979797>, <User: 8888888888>, <User: 9989787878>]>', to=settings.AUTH_USER_MODEL),
        ),
    ]
