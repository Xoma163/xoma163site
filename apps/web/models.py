from django.db import models


# Create your models here.

class Session(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"
        ordering = ['id']


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    session = models.ForeignKey(Session, verbose_name="Сессия", on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name="Имя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id']


class Tare(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тара"
        verbose_name_plural = "Тары"
        ordering = ['id']


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    session = models.ForeignKey(Session, verbose_name="Сессия", on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name="Название", null=True, blank=True, default="")
    count = models.PositiveIntegerField(verbose_name="Количество", default=0)
    tare = models.ForeignKey(Tare, verbose_name="Тара", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name="Стоимость", default=0)
    user = models.ForeignKey(User, verbose_name="Купил", on_delete=models.SET_NULL, null=True, blank=True)
    is_bought = models.BooleanField(verbose_name="Куплено", default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['id']


class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    session = models.ForeignKey(Session, verbose_name="Заказ", on_delete=models.CASCADE)

    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Туса"
        verbose_name_plural = "Тусы"
        ordering = ['id']

    def __str__(self):
        return str(self.session) + " " + str(self.product)
