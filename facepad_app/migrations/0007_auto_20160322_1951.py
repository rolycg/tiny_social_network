# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facepad_app', '0006_auto_20160322_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['date', 'pk'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Posted on'),
        ),
    ]
