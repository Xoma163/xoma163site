# Generated by Django 2.2.5 on 2020-04-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0020_auto_20200426_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='timezone',
            field=models.CharField(max_length=30, null=True, verbose_name='Временная зона UTC'),
        ),
    ]
