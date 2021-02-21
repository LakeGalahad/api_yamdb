from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    """Роли пользователей."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Расширение модели пользователей."""
    bio = models.TextField('О себе', max_length=500, blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=100,
                                         blank=True)
    email = models.EmailField('Почта', unique=True, blank=False)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
