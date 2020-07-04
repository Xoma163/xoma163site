import random

from django.db import models

# Create your models here.
from apps.API_VK.models import VkUser


def random_digits():
    digits_count = 6
    return str(random.randint(10 ** (digits_count - 1), 10 ** digits_count - 1))


class TgUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user_id = models.CharField(verbose_name='ID пользователя', max_length=20)
    vk_user = models.ForeignKey(VkUser, verbose_name="ВК Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_active(self):
        return self.vk_user is not None

    def __str__(self):
        return str(self.vk_user)


class TgTempUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    vk_user = models.ForeignKey(VkUser, verbose_name="Вк юзер", on_delete=models.CASCADE, null=True, blank=True)
    tg_user = models.ForeignKey(TgUser, verbose_name="Тг юзер", on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(verbose_name="Код подтверждения", default=random_digits, max_length=6)
    tries = models.IntegerField(verbose_name="Кол-во попыток", default=5)

    class Meta:
        verbose_name = "Временный пользователь"
        verbose_name_plural = "Временные пользователи"

    def __str__(self):
        return str(self.vk_user)
