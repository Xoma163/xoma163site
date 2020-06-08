# Generated by Django 2.2.5 on 2020-05-01 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0029_meme_uses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiolist',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='city',
            name='timezone',
            field=models.ForeignKey(default='', max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='service.TimeZone', verbose_name='Временная зона UTC'),
        ),
        migrations.AlterField(
            model_name='counter',
            name='chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='API_VK.VkChat', verbose_name='Чат'),
        ),
        migrations.AlterField(
            model_name='latermessage',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='latermessage',
            name='message_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='message_author_latermessages', to='API_VK.VkUser',
                                    verbose_name='Автор сообщения'),
        ),
        migrations.AlterField(
            model_name='latermessage',
            name='message_bot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='API_VK.VkBot', verbose_name='Автор сообщения(бот)'),
        ),
        migrations.AlterField(
            model_name='meme',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='notify',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API_VK.VkUser',
                                    verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='notify',
            name='chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='API_VK.VkChat', verbose_name='Чат'),
        ),
    ]
