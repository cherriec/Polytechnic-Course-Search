# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 10:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursesearch', '0004_auto_20170322_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='L1R4Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesearch.Category'),
        ),
        migrations.AlterField(
            model_name='course',
            name='l1r4group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesearch.L1R4Group'),
        ),
        migrations.AlterField(
            model_name='course',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesearch.School'),
        ),
    ]
