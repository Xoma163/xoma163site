# Generated by Django 2.2.5 on 2020-05-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0032_cat_to_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='to_send',
            field=models.BooleanField(default=False, verbose_name='Ещё не было'),
        ),
    ]
