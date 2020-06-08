# Generated by Django 2.2.5 on 2020-04-19 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('API_VK', '0002_auto_20200405_2312'),
        ('service', '0012_auto_20200419_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiolist',
            options={'ordering': ['name'], 'verbose_name': 'аудиозапись', 'verbose_name_plural': 'аудиозаписи'},
        ),
        migrations.AlterModelOptions(
            name='latermessage',
            options={'verbose_name': 'Потом сообщение', 'verbose_name_plural': 'Потом сообщения'},
        ),
        migrations.AddField(
            model_name='latermessage',
            name='message_bot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API_VK.VkChat',
                                    verbose_name='Автор сообщения(бот)'),
        ),
    ]
