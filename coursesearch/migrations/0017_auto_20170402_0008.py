# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesearch', '0016_auto_20170401_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B3', 'B3'), ('B4', 'B4'), ('C5', 'C5'), ('C6', 'C6'), ('D7', 'D7'), ('E8', 'E8'), ('F9', 'F9')], max_length=2),
        ),
    ]
