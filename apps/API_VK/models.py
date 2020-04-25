import random

from django.contrib.auth.models import Group
from django.db import models


class VkChat(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    chat_id = models.CharField(verbose_name='ID чата', max_length=20, default="")
    name = models.CharField(verbose_name='Название', max_length=40, default="", blank=True)
    admin = models.ForeignKey('VkUser', verbose_name='Админ конфы', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["chat_id"]

    def __str__(self):
        return str(self.name)


class VkUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')

    user_id = models.CharField(verbose_name='ID пользователя', max_length=20)
    name = models.CharField(verbose_name='Имя', max_length=40, default="")
    surname = models.CharField(verbose_name='Фамилия', max_length=40, default="")
    nickname = models.CharField(verbose_name="Никнейм", max_length=40, blank=True, default="")
    nickname_real = models.CharField(verbose_name="Прозвище", max_length=40, blank=True, default="")
    gender = models.CharField(verbose_name='Пол', max_length=2, blank=True, default="")
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    # Здесь такой странный ForeignKey потому что проблема импортов
    city = models.ForeignKey('service.City', verbose_name='Город', null=True, blank=True, on_delete=models.SET_NULL)
    chats = models.ManyToManyField(VkChat, verbose_name="Чаты", blank=True)

    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(Group, verbose_name="Группы")

    send_notify_to = models.ManyToManyField('self', verbose_name="Отправление уведомлений", blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name", "surname"]

    def __str__(self):
        return str(self.name + " " + self.surname)


class VkBot(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    bot_id = models.CharField(verbose_name='ID бота', max_length=20)
    name = models.CharField(verbose_name='Имя', max_length=40, default="")

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Боты"
        ordering = ["id"]

    def __str__(self):
        return str(self.name)


class Log(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True)
    author = models.ForeignKey(VkUser, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    event = models.CharField(verbose_name='Событие', choices=(('home', 'дома'),
                                                              ('work', 'работа'),
                                                              ('university', 'университет'),
                                                              ('somewhere', 'где-то')),
                             max_length=20,
                             null=True)
    msg = models.CharField(verbose_name='Сообщение', max_length=2000)
    success = models.BooleanField(verbose_name='Отправлено', default=False)

    @classmethod
    def create(cls, imei, author, event, msg, success):
        log = cls(imei=imei, author=author, event=event, msg=msg, success=success)
        return log

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Журнал событий"
        ordering = ["-date"]

    def __str__(self):
        return str(self.id)


class QuoteBook(models.Model):
    text = models.TextField(verbose_name="Текст", max_length=5000)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    peer_id = models.CharField(verbose_name='ID чата', max_length=20, default=0)

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        ordering = ['-date']

    def __str__(self):
        return str(self.text)


class Words(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')

    m1 = models.CharField(verbose_name="Мужской", max_length=500, null=True)
    f1 = models.CharField(verbose_name="Женский", max_length=500, null=True)
    n1 = models.CharField(verbose_name="Средний", max_length=500, null=True)
    mm = models.CharField(verbose_name="Множественный мужской", max_length=500, null=True)
    fm = models.CharField(verbose_name="Множественный женский", max_length=500, null=True)

    type = models.CharField(verbose_name='Тип', choices=(('bad', 'Плохое'), ('good', 'Хорошее')), default="bad",
                            max_length=10)

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['type', 'id']

    def __str__(self):
        return str(self.m1)


class APIUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user_id = models.CharField(verbose_name="ID пользователя", max_length=100)
    vk_user = models.ForeignKey(VkUser, verbose_name="Вк юзер", on_delete=models.SET_NULL, null=True, blank=True)
    vk_chat = models.ForeignKey(VkChat, verbose_name="Вк чат", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "API Пользователь"
        verbose_name_plural = "API Пользователи"

    def __str__(self):
        return str(self.vk_user)


def random_digits():
    digits_count = 6
    return str(random.randint(10 ** (digits_count - 1), 10 ** digits_count - 1))


class APITempUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user_id = models.CharField(verbose_name="ID пользователя", max_length=100)
    vk_user = models.ForeignKey(VkUser, verbose_name="Вк юзер", on_delete=models.SET_NULL, null=True, blank=True)
    vk_chat = models.ForeignKey(VkChat, verbose_name="Вк чат", on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(verbose_name="Код подтверждения", default=random_digits, max_length=6)
    tries = models.IntegerField(verbose_name="Кол-во попыток", default=5)

    class Meta:
        verbose_name = "API Временный пользователь"
        verbose_name_plural = "API Временные пользователи"

    def __str__(self):
        return str(self.vk_user)
