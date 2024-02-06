from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=250, blank=False, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Краткое описание')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    cookingSteps = models.TextField(verbose_name='Способ приготовления')
    cook_time = models.PositiveSmallIntegerField(default=0, verbose_name='Время приготовления')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='recipes',
                               null=True, default=None, verbose_name='Автор рецепта')
    image = models.ImageField(upload_to='img_dish/',
                              blank=True, verbose_name='Фото блюда') # upload_to='img_dish/%Y/%m/%d/'
    categories = models.ManyToManyField(Category, related_name='categories', verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

