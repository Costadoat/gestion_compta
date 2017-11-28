# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='familymember',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interventions.Profile'),
        ),
    ]
