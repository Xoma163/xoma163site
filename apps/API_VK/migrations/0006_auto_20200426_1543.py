# Generated by Django 2.2.5 on 2020-04-26 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('API_VK', '0005_remove_quotebook_peer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkchat',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='API_VK.VkUser', verbose_name='Админ'),
        ),
    ]
