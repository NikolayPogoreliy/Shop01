# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-02 21:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20161130_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_material',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_material', to='catalog.Material', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_pubDate',
            field=models.DateField(default=datetime.date(2016, 12, 2), help_text='Для отложенной публикации установите будущую дату', verbose_name='Дата публикации на сайте'),
        ),
    ]