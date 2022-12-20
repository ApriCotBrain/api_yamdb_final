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
        default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
