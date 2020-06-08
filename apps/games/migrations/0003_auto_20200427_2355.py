# Generated by Django 2.2.5 on 2020-04-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0002_auto_20200417_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codenamessession',
            name='next_step',
            field=models.CharField(blank=True,
                                   choices=[('red', 'Синие'), ('blue', 'Красные'), ('blue_wait', 'Капитан синих'),
                                            ('red_wait', 'Капитан красных')], default='blue_wait', max_length=10,
                                   null=True, verbose_name='Следующий шаг'),
        ),
    ]
