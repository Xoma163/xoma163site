# Generated by Django 2.2.13 on 2020-06-21 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('API_VK', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logger_name', models.CharField(max_length=100, verbose_name='Логгер')),
                ('level', models.PositiveSmallIntegerField(
                    choices=[(0, 'NOTSET'), (10, 'DEBUG'), (20, 'INFO'), (30, 'WARNING'), (40, 'ERROR'), (50, 'FATAL')],
                    db_index=True, default=40, verbose_name='Уровень')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('vk_event', models.TextField(blank=True, null=True, verbose_name='Запрос пользователя')),
                ('user_msg', models.TextField(blank=True, null=True, verbose_name='Сообщение пользователя')),
                ('msg', models.TextField(verbose_name='Сообщение')),
                ('result', models.TextField(blank=True, null=True, verbose_name='Результат выполнения')),
                ('exception', models.TextField(blank=True, null=True, verbose_name='Ошибка')),
                ('traceback', models.TextField(blank=True, null=True, verbose_name='Traceback')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API_VK.VkChat',
                                           verbose_name='Чат')),
                ('sender',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API_VK.VkUser',
                                   verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'ordering': ('-create_datetime',),
            },
        ),
    ]
