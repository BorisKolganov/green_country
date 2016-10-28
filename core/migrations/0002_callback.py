# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-28 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='\u0424\u0418\u041e')),
                ('phone', models.CharField(max_length=15, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('checked', models.BooleanField(default=False, verbose_name='\u041f\u0435\u0440\u0435\u0437\u0432\u043e\u043d\u0438\u043b\u0438')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e \u0432')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d\u043e \u0432')),
            ],
            options={
                'verbose_name': '\u041e\u0431\u0440\u0430\u0442\u043d\u044b\u0439 \u0437\u0432\u043e\u043d\u043e\u043a',
                'verbose_name_plural': '\u041e\u0431\u0440\u0430\u0442\u043d\u044b\u0435 \u0437\u0432\u043e\u043d\u043a\u0438',
            },
        ),
    ]
