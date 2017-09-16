# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesearch', '0009_remove_course_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('ENG', 'Engineering'), ('SCI', 'Science'), ('BIZ', 'Business'), ('DES', 'Design'), ('MIT', 'Media & IT'), ('HSS', 'Humanities')], max_length=3),
        ),
    ]
