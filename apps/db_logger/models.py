import logging

from django.db import models

from apps.API_VK.models import VkUser, VkChat


class Logger(models.Model):
    LOG_LEVELS = (
        (logging.NOTSET, 'NOTSET'),
        (logging.DEBUG, "DEBUG"),
        (logging.INFO, "INFO"),
        (logging.WARNING, "WARNING"),
        (logging.ERROR, "ERROR"),
        (logging.FATAL, "FATAL"),
    )

    logger_name = models.CharField("Логгер", max_length=100)
    level = models.PositiveSmallIntegerField("Уровень", choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    vk_event = models.TextField("Запрос пользователя", blank=True, null=True)

    sender = models.ForeignKey(VkUser, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(VkChat, verbose_name="Чат", on_delete=models.SET_NULL, null=True)
    user_msg = models.TextField("Сообщение пользователя", blank=True, null=True)
    msg = models.TextField("Сообщение")

    result = models.TextField("Результат выполнения", blank=True, null=True)
    exception = models.TextField("Ошибка", blank=True, null=True)
    traceback = models.TextField(blank=True, null=True, verbose_name="Traceback")

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ('-create_datetime',)
        verbose_name = "Лог"
        verbose_name_plural = 'Логи'
