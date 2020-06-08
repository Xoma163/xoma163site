# Generated by Django 2.2.5 on 2020-05-29 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('API_VK', '0010_auto_20200523_1346'),
        ('service', '0049_delete_wakeonlanuserdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WakeOnLanUserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('ip', models.CharField(max_length=16, verbose_name='IP')),
                ('port', models.SmallIntegerField(verbose_name='Порт')),
                ('mac', models.CharField(max_length=17, verbose_name='MAC адрес')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                           verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'WOL устройство',
                'verbose_name_plural': 'WOL устройства',
            },
        ),
    ]
