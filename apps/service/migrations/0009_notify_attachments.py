# Generated by Django 2.2.5 on 2020-04-18 17:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0008_auto_20200417_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='attachments',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='Вложения'),
        ),
    ]
