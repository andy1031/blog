# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-14 00:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190514_0849'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([]),
        ),
    ]
