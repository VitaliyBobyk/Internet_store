from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Категорія', max_length=150)
    description = models.TextField('Опис')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Item(models.Model):
    title = models.CharField('Назва товару', max_length=150)
    old_price = models.CharField('Стара ціна', blank=True, max_length=150)
    new_price = models.CharField('Нова ціна', max_length=150)
    color = models.CharField('Колір', max_length=150, default='Black')
    brand = models.CharField('Виробник', max_length=150, default='Apple')
    diagonal = models.CharField('Діагональ', max_length=150, default='4,5\'', blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Картинка основна')
    image_two = models.ImageField('Картинка - 2')
    image_three = models.ImageField('Картинка - 3')
    image_hover = models.ImageField('Картника по наведенню')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hotdeal = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'


