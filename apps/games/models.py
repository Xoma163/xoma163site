from django.db import models

from apps.API_VK.models import VkUser, VkChat


class Gamer(models.Model):
    user = models.ForeignKey(VkUser, verbose_name="Игрок", on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(verbose_name="Очки", default=0)

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


    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"
        ordering = ["chat", "user"]

    def __str__(self):
        return str(self.chat) + " " + str(self.user)
