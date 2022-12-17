from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'О пользователе',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        blank=False    # Возможно тут True, надо проверить с api
    )
    # conf_code?

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
