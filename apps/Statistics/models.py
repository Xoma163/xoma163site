from django.db import models


class Statistics(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    command = models.CharField(verbose_name='Команда', max_length=20)
    count_queries = models.IntegerField(verbose_name='Количество запросов', default=0)

    class Meta:
        verbose_name = "команду"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return str(self.command)
