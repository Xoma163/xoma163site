# Generated by Django 2.2.5 on 2020-05-23 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('API_VK', '0010_auto_20200523_1346'),
        ('service', '0037_latermessagesession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='latermessage',
            name='author',
        ),
        migrations.AddField(
            model_name='latermessagesession',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
    ]
