import os
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.contrib.postgres.fields import JSONField
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.API_VK.models import VkChat, VkUser, VkBot
from xoma163site.settings import MEDIA_ROOT


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


# ToDo: переделать на requests
def get_image_from_url(url):
    if url:
        ext = url.split('.')[-1]
        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        return ext, img_temp


class Cat(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='service/cats/', verbose_name="Изображение")
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "кот"
        verbose_name_plural = "коты"

    def __str__(self):
        return str(self.id)

    def save_remote_image(self, url):
        if not self.image:
            ext, image = get_image_from_url(url)
            self.image.save(f"cat.{ext}", File(image))
        self.save()

    def preview(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<img src="{0}" width="150"/>'.format(self.image.url))
        else:
            return '(Нет изображения)'


class Meme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название", max_length=1000, default="")
    link = models.CharField(verbose_name="Ссылка", max_length=1000, default="", null=True, blank=True)
    image = models.ImageField(upload_to='service/memes/', verbose_name="Изображение", null=True, blank=True)
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "мем"
        verbose_name_plural = "мемы"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def save_remote_image(self, url, ext_image=None):
        if not self.image:
            ext, image = get_image_from_url(url)
            if ext_image:
                ext = ext_image
            self.image.save(f"{self.name}.{ext}", File(image))
        self.save()

    def preview(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<img src="{0}" width="150"/>'.format(self.image.url))
        else:
            return '(Нет изображения)'


@receiver(pre_delete, sender=Cat, dispatch_uid='question_delete_signal')
@receiver(pre_delete, sender=Meme, dispatch_uid='question_delete_signal')
def log_deleted_question(sender, instance, using, **kwargs):
    if instance.image:
        delete_path = f'{MEDIA_ROOT}/{instance.image}'
        try:
            os.remove(delete_path)
        except FileNotFoundError:
            print("Warn: Кот/Мем удалён, но файл картинки не найден")


class Notify(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(verbose_name="Дата напоминания")
    text = models.CharField(verbose_name="Текст/команда", max_length=1000, default="")
    text_for_filter = models.CharField(verbose_name="Текст для поиска", max_length=1000, default="")
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, on_delete=models.SET_NULL, blank=True)
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    repeat = models.BooleanField(verbose_name="Повторять", default=False)
    attachments = JSONField(null=True, verbose_name="Вложения", blank=True)

    class Meta:
        verbose_name = "напоминание"
        verbose_name_plural = "напоминания"
        ordering = ["date"]

    def __str__(self):
        return str(self.text)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название", max_length=100)
    synonyms = models.CharField(verbose_name="Похожие названия", max_length=300)
    timezone = models.CharField(verbose_name="Временная зона UTC", null=True, max_length=30)
    lat = models.FloatField(verbose_name="Широта", null=True)
    lon = models.FloatField(verbose_name="Долгота", null=True)

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class AudioList(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="Название", max_length=300)
    attachment = models.CharField(verbose_name="Вложение", max_length=100, default="", null=True, blank=True)

    class Meta:
        verbose_name = "аудиозапись"
        verbose_name_plural = "аудиозаписи"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class LaterMessage(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    message_author = models.ForeignKey(VkUser, verbose_name="Автор сообщения", on_delete=models.SET_NULL, null=True,
                                       related_name="message_author_%(class)ss", blank=True)
    message_bot = models.ForeignKey(VkBot, verbose_name="Автор сообщения(бот)", on_delete=models.SET_NULL, null=True,
                                    blank=True)
    text = models.CharField(verbose_name="Текст", max_length=300, blank=True)
    date = models.DateTimeField(verbose_name="Дата сообщения")
    attachments = JSONField(null=True, verbose_name="Вложения", blank=True)

    class Meta:
        verbose_name = "Потом сообщение"
        verbose_name_plural = "Потом сообщения"
        ordering = ['-date']

    def __str__(self):
        return f"{self.id}. {self.author}"


class Donations(models.Model):
    username = models.CharField(verbose_name="Имя", max_length=100, blank=True)
    amount = models.CharField(verbose_name="Количество", max_length=10, blank=True)
    currency = models.CharField(verbose_name="Валюта", max_length=30, blank=True)
    message = models.CharField(verbose_name="Сообщение", max_length=1000, blank=True)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"
        ordering = ['-date']

    def __str__(self):
        return f"{self.username}. {self.amount}"
