# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-24 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20161224_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_views',
            field=models.PositiveSmallIntegerField(default=0, editable=False, null=True, verbose_name='Колличество просмотров'),
        ),
    ]