from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    group = models.CharField('Группа', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'Без имени'})"
