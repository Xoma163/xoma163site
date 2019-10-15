from django.db import models


class TelegramTrustIMEI(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    imei = models.CharField(verbose_name='IMEI', max_length=20)
    name = models.CharField(verbose_name='Владелец', max_length=20)
    is_active = models.BooleanField(verbose_name='Активность', default=False)

    class Meta:
        verbose_name = "устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return str(self.name)


class TelegramChatId(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    chat_id = models.CharField(verbose_name='ID чата', max_length=20)
    name = models.CharField(verbose_name='Владелец', max_length=20)
    is_active = models.BooleanField(verbose_name='Активность', default=False)

    class Meta:
        verbose_name = "доверенный чат"
        verbose_name_plural = "Доверенные чаты"

    def __str__(self):
        return str(self.name)


# datetime object containing current date and time
class Log(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True)
    author = models.ForeignKey(TelegramTrustIMEI, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    event = models.CharField(verbose_name='Событие', choices=(('home', 'дома'), ('work', 'на работе')), max_length=20,
                             null=True)
    msg = models.CharField(verbose_name='Сообщение', max_length=2000)
    success = models.BooleanField(verbose_name='Отправлено', default=False)

    @classmethod
    def create(cls, imei, author, event, msg, success):
        log = cls(imei=imei, author=author, event=event, msg=msg, success=success)
        # do something with the book
        return log

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "Журнал событий"

    def __str__(self):
        return str(self.id)
