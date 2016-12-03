# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 15:10
from __future__ import unicode_literals

import Shop01.utils
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20161202_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='manufacturer_logo',
            field=models.ImageField(blank=True, default='', null=True, upload_to=Shop01.utils.ImageUploader.make_upload_path, verbose_name='Логотип производителя'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_pubDate',
            field=models.DateField(default=datetime.date(2016, 12, 3), help_text='Для отложенной публикации установите будущую дату', verbose_name='Дата публикации на сайте'),
        ),
    ]
