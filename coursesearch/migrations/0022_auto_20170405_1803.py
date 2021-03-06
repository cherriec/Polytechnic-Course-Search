# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 10:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursesearch', '0021_remove_profile_targets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesearch.Course')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesearch.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='targets',
            field=models.ManyToManyField(through='coursesearch.Target', to='coursesearch.Course'),
        ),
    ]
