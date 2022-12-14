from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title_category',
        verbose_name='Категория произведения'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title_genre',
        verbose_name='Жанр произведения'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Год произведения'
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        constraints = [
            models.UniqueConstraint(fields=['name', 'category'],
                                    name='unique_title_category')
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
