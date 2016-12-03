# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 15:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20161203_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_manufacturer', to='catalog.Manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_model', to='catalog.ProductModel', verbose_name='Модель'),
        ),
    ]
