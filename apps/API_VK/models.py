from django.db import models


class Stream(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    link = models.URLField(verbose_name='Ссылка на стрим')

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стрим"

    def __str__(self):
        return str(self.link)


class VkUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')

    user_id = models.CharField(verbose_name='ID пользователя', max_length=20)
    name = models.CharField(verbose_name='Имя', max_length=40, default="")
    surname = models.CharField(verbose_name='Фамилия', max_length=40, default="")
    gender = models.CharField(verbose_name='Пол', max_length=6, blank=True, default="")

    get_notify_from = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Получение уведомлений от",
                                        null=True, blank=True)
    send_notify = models.BooleanField(verbose_name='Отправлять сведения передвижения', default=False)
    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True, blank=True)

    is_admin = models.BooleanField(verbose_name='Админ', default=False)
    is_student = models.BooleanField(verbose_name='Студент', default=False)
    is_banned = models.BooleanField(verbose_name='Забанен', default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.name + " " + self.surname)


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
        # do something with the book
        return log

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Журнал событий"

    def __str__(self):
        return str(self.id)


class PetrovichUser(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat_id = models.CharField(verbose_name='ID чата', max_length=20)
    wins = models.IntegerField(verbose_name="Побед в Петровиче", default=0)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self):
        return str(self.user)


class PetrovichGames(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat_id = models.CharField(verbose_name='ID чата', max_length=20, default=0)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, editable=True)

    class Meta:
        verbose_name = "Игра Петровича"
        verbose_name_plural = "Игры Петровича"

    def __str__(self):
        return str(self.user)


class QuoteBook(models.Model):
    text = models.CharField(verbose_name="Текст", max_length=10000)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)
    # author = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    username = models.CharField(verbose_name='Имя пользователя', max_length=40, default="")
    user_id = models.CharField(verbose_name='ID автора', max_length=20, default=0)
    peer_id = models.CharField(verbose_name='ID чата', max_length=20, default=0)

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return str(self.text)
