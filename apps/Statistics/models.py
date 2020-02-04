from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from django.db import models

from apps.API_VK.models import VkChat


class Statistic(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    command = models.CharField(verbose_name='Команда', max_length=20)
    count_queries = models.IntegerField(verbose_name='Количество запросов', default=0)

    class Meta:
        verbose_name = "статистику"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return str(self.command)


class Issue(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    text = models.TextField(verbose_name='Фича', max_length=5000)

    class Meta:
        verbose_name = "ишю"
        verbose_name_plural = "Ишюс"

    def __str__(self):
        return str(self.text)


class Service(models.Model):
    name = models.CharField(primary_key=True, verbose_name="Имя", max_length=50)
    value = models.CharField(verbose_name="Значение", max_length=1000, default="", null=True)
    update_datetime = models.DateTimeField(verbose_name="Дата создания", auto_now=True)

    class Meta:
        verbose_name = "сервис"
        verbose_name_plural = "сервисы"

    def __str__(self):
        return self.name


class Counter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Имя", max_length=50, blank=True)
    count = models.IntegerField(verbose_name="Количество", default=0)
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "счётчик"
        verbose_name_plural = "счётчики"

    def __str__(self):
        return self.name


class Cat(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='service/cats/', verbose_name="Изображение")

    class Meta:
        verbose_name = "кот"
        verbose_name_plural = "коты"

    def __str__(self):
        return str(self.id)

    def get_remote_image(self, url):
        if url and not self.image:
            format = url.split('.')[-1]
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(url).read())
            img_temp.flush()
            self.image.save(f"cat.{format}", File(img_temp))
        self.save()

    def preview(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<img src="{0}" width="150"/>'.format(self.image.url))
        else:
            return '(Нет изображения)'
