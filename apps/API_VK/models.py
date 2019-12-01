from django.db import models


class StreamModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    link = models.URLField(verbose_name='Ссылка на стрим')

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стрим"
        ordering = ["id"]

    def __str__(self):
        return str(self.link)


class VkChat(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    chat_id = models.CharField(verbose_name='ID чата', max_length=20)
    name = models.CharField(verbose_name='Название', max_length=40, default="", blank=True)

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["id"]

    def __str__(self):
        return str(self.name)


class VkUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')

    user_id = models.CharField(verbose_name='ID пользователя', max_length=20)
    name = models.CharField(verbose_name='Имя', max_length=40, default="")
    surname = models.CharField(verbose_name='Фамилия', max_length=40, default="")
    nickname = models.CharField(verbose_name="Никнейм", max_length=40, blank=True, default="")
    gender = models.CharField(verbose_name='Пол', max_length=2, blank=True, default="")
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=40, blank=True, default="")

    chats = models.ManyToManyField(VkChat, verbose_name="Чаты", blank=True)

    get_notify_from = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Получение уведомлений от",
                                        null=True, blank=True)
    send_notify = models.BooleanField(verbose_name='Отправлять сведения передвижения', default=False)
    imei = models.CharField(verbose_name='IMEI', max_length=20, null=True, blank=True)

    is_admin = models.BooleanField(verbose_name='Админ', default=False)
    is_moderator = models.BooleanField(verbose_name='Модератор', default=False)
    is_student = models.BooleanField(verbose_name='Студент', default=False)
    is_banned = models.BooleanField(verbose_name='Забанен', default=False)

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


class PetrovichUser(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, blank=True, on_delete=models.SET_NULL)
    wins = models.IntegerField(verbose_name="Побед в Петровиче", default=0)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ["user"]

    def __str__(self):
        return str(self.user)


class PetrovichGames(models.Model):
    user = models.ForeignKey(VkUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    chat = models.ForeignKey(VkChat, verbose_name='Чат', null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, editable=True)

    class Meta:
        verbose_name = "Игра Петровича"
        verbose_name_plural = "Игры Петровича"
        ordering = ['-date']

    def __str__(self):
        return str(self.user)


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

    m1 = models.CharField(verbose_name="Мужской", max_length=100, null=True)
    f1 = models.CharField(verbose_name="Женский", max_length=100, null=True)
    n1 = models.CharField(verbose_name="Средний", max_length=100, null=True)
    mm = models.CharField(verbose_name="Множественный мужской", max_length=100, null=True)
    fm = models.CharField(verbose_name="Множественный женский", max_length=100, null=True)

    type = models.CharField(verbose_name='Событие', choices=(('bad', 'Плохое'), ('good', 'Хорошее')), default="bad",
                            max_length=10)

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['m1']

    def __str__(self):
        return str(self.m1)
