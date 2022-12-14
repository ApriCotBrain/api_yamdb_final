from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
DEFAULT_CHOICES = (
    ('10', '10'),
    ('9', '9'),
    ('8', '8'),
    ('7', '7'),
    ('6', '6'),
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
    ('0', '0')
)


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


class Reviews(models.Model):
    title_id = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name='ID title'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        max_length=2,
        choices=DEFAULT_CHOICES,
        verbose_name='title score'
    )
    # Или юзать скор верхний, если вы одобрите, или нижний, для целочисленного
    # вывода,
    # если я правильно разобрался в документации по django лучше юзать нижний

    class Score(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
        six = 6
        seven = 7
        eight = 8
        nine = 9
        ten = 10

    score = models.IntegerField(choices=Score.choices)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


"""class Comment(models.Model):
    title_id = models.ForeignKey(
        unique=True,
        null=False,
        verbose_name='ID title'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария',
    )
    review_id = models.ForeignKey(
        unique=True,
        null=False,
        verbose_name='ID review'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'"""
