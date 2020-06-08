# Generated by Django 2.2.5 on 2020-05-23 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('API_VK', '0010_auto_20200523_1346'),
        ('service', '0043_delete_youtubesubscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeSubscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=100, verbose_name='ID канала')),
                ('title', models.CharField(max_length=100, verbose_name='Название канала')),
                ('date', models.DateTimeField(verbose_name='Дата последней публикации')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                             verbose_name='Автор')),
                ('chat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                           to='API_VK.VkChat', verbose_name='Чат')),
            ],
            options={
                'verbose_name': 'Подписка ютуба',
                'verbose_name_plural': 'Подписки ютуба',
            },
        ),
    ]
