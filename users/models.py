from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Путь к аватаркам
    bio = models.TextField(null=True, blank=True)  # О себе
    birth_date = models.DateField(null=True, blank=True)  # Дата рождения
    location = models.CharField(max_length=30, null=True, blank=True)  # Местоположение
    phone = models.CharField(max_length=30, null=True, blank=True)  # Телефон
    is_online = models.BooleanField(default=False)  # Флаг онлайна
    is_verified = models.BooleanField(default=False)  # Флаг верификации
    is_active = models.BooleanField(default=True)  # Флаг активности
    is_staff = models.BooleanField(default=False)  # Флаг персонала
    is_superuser = models.BooleanField(default=False)  # Флаг суперпользователя
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания
    updated_at = models.DateTimeField(auto_now=True)  # Время обновления

    def __str__(self):
        return self.username