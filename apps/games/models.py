import json

from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.API_VK.models import VkUser, VkChat


class Gamer(models.Model):
    user = models.ForeignKey(VkUser, verbose_name="Игрок", on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(verbose_name="Очки", default=0)
    tic_tac_toe_points = models.IntegerField(verbose_name="Очки крестики-нолики", default=0)
    codenames_points = models.IntegerField(verbose_name="Очки коднеймса", default=0)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ["user"]

    def __str__(self):
        return str(self.user)


class Rate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(VkUser, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(VkChat, verbose_name="Чат", on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField(verbose_name="Ставка")
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    random = models.BooleanField(verbose_name="Случайная", default=False)

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"
        ordering = ["chat", "date"]

    def __str__(self):
        return str(self.chat) + " " + str(self.user)


# class RateDelete(models.Model):
#     id = models.AutoField(primary_key=True, verbose_name='ID')
#     chat = models.ForeignKey(VkChat, verbose_name="Чат", on_delete=models.SET_NULL, null=True)
#     message_id = models.IntegerField(verbose_name="ID сообщения")


class PetrovichUser(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, blank=True, on_delete=models.SET_NULL)
    wins = models.IntegerField(verbose_name="Побед в Петровиче", default=0)
    active = models.BooleanField(verbose_name="Активность", default=True)

    class Meta:
        verbose_name = "Петрович игрок"
        verbose_name_plural = "Петрович игроки"
        ordering = ["user"]

    def __str__(self):
        return str(self.user)


class PetrovichGames(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, editable=True)

    class Meta:
        verbose_name = "Петровича игра"
        verbose_name_plural = "Петрович игры"
        ordering = ['-date']

    def __str__(self):
        return str(self.user)


def get_default_board():
    return json.dumps([['', '', ''], ['', '', ''], ['', '', '']])


class TicTacToeSession(models.Model):
    user1 = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь *",
                              related_name="user1_%(class)ss")
    user2 = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь o",
                              related_name="user2_%(class)ss")
    next_step = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name="Следующий шаг",
                                  related_name="next_%(class)ss")
    board = JSONField(null=True, verbose_name="Поле", default=get_default_board)

    class Meta:
        verbose_name = "Крестики-нолики сессия"
        verbose_name_plural = "Крестики-нолики сессии"
        ordering = ['-next_step']

    def __str__(self):
        return str(self.user1) + " " + str(self.user2)


class CodenamesUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(VkUser, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(VkChat, verbose_name="Чат", on_delete=models.SET_NULL, null=True)
    command_list = [('blue', "Синие"), ('red', "Красные")]
    command = models.CharField('Команда', choices=command_list, max_length=4, null=True, blank=True)
    role_list = [('captain', "Капитан"), ('player', "Игрок")]
    role = models.CharField('Команда', choices=role_list, default='player', max_length=7)

    class Meta:
        verbose_name = "Коднеймс игрок"
        verbose_name_plural = "Коднеймс игроки"
        ordering = ["chat"]

    def __str__(self):
        return str(self.user)


class CodenamesSession(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    chat = models.ForeignKey(VkChat, verbose_name="Чат", on_delete=models.SET_NULL, null=True)
    # red, blue, red_wait, blue_wait, red_extra, blue_extra
    next_step_list = [('red', "Синие"), ('blue', "Красные"), ('blue_wait', "Капитан синих"),
                      ('red_extra', "Капитан красных")]
    next_step = models.CharField(verbose_name="Следующий шаг", null=True, blank=True, choices=next_step_list,
                                 default="blue_wait", max_length=10)
    count = models.IntegerField(verbose_name="Загадано слов", null=True, blank=True)
    word = models.CharField(verbose_name="Загаданное слово", null=True, blank=True, max_length=20)
    # [[{"Слово":"type"},{"Слово":"type"},...],...] type='red','blue','neutral','death'
    board = JSONField(null=True, verbose_name="Поле", default=get_default_board)

    class Meta:
        verbose_name = "Коднеймс сессия"
        verbose_name_plural = "Коднеймс сессии"
        ordering = ["chat"]

    def __str__(self):
        return str(self.id)
