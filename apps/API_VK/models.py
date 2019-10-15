from django.db import models


class TrustIMEI(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    imei = models.CharField(verbose_name='IMEI', max_length=20)
    name = models.CharField(verbose_name='Владелец', max_length=20)
    is_active = models.BooleanField(verbose_name='Активность', default=False)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return str(self.name)


class VkChatId(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    chat_id = models.CharField(verbose_name='ID чата', max_length=20)
    name = models.CharField(verbose_name='Владелец', max_length=20)
    is_active = models.BooleanField(verbose_name='Активность', default=False)
    is_admin = models.BooleanField(verbose_name='Админ', default=False)

    class Meta:
        verbose_name = "Доверенный чат"
        verbose_name_plural = "Доверенные чаты"

    def __str__(self):
        return str(self.name)


# datetime object containing current date and time
class Log(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True)
    author = models.ForeignKey(TrustIMEI, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    event = models.CharField(verbose_name='Событие', choices=(
        ('home', 'дома'), ('work', 'работа'), ('university', 'университет'), ('somewhere', 'где-то')), max_length=20,
                             null=True)
    msg = models.CharField(verbose_name='Сообщение', max_length=2000)
    success = models.BooleanField(verbose_name='Отправлено', default=False)

    @classmethod
    def create(cls, imei, author, event, msg, success):
        log = cls(imei=imei, author=author, event=event, msg=msg, success=success)
        # do something with the book
        return log

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Журнал событий"

    def __str__(self):
        return str(self.id)


class Stream(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    link = models.URLField(verbose_name='Ссылка на стрим')

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return str(self.link)


class VkUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user_id = models.CharField(verbose_name='ID пользователя', max_length=20)
    chat_id = models.CharField(verbose_name='ID чата', max_length=20)
    username = models.CharField(verbose_name='Имя пользователя', max_length=40)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.username)


class Winners(models.Model):
    winner = models.ForeignKey(VkUser, verbose_name="Победитель", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    chat_id = models.CharField(verbose_name='ID чата', max_length=20, default=0)

    class Meta:
        verbose_name = "Победитель"
        verbose_name_plural = "Победители"

    def __str__(self):
        return str(self.winner)


class QuoteBook(models.Model):
    text = models.CharField(verbose_name="Текст", max_length=10000)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=40, default="")
    user_id = models.CharField(verbose_name='ID автора', max_length=20, default=0)
    peer_id = models.CharField(verbose_name='ID чата', max_length=20, default=0)

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return str(self.text)


class UsersCache(models.Model):
    user_id = models.CharField(verbose_name='ID', max_length=20, default=0)
    name = models.CharField(verbose_name='Имя', max_length=40, default="")
    surname = models.CharField(verbose_name='Фамилия', max_length=40, default="")
    gender = models.CharField(verbose_name='Пол', max_length=1, default="0")  # 1 тян, 2 - кун, 0 - хз по-моему

    class Meta:
        verbose_name = "Кэшированный пользователь"
        verbose_name_plural = "Кэшированные пользователи"

    def __str__(self):
        return str(self.name + " " + self.surname)
