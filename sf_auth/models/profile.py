# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    # Автоматически генерируемый UUID
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Связь с пользователем
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Основное фото профиля
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        help_text="Основное фото профиля"
    )

    # Дополнительные поля
    second_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Спорт (внешний ключ)
    main_sport = models.ForeignKey(
        'sf_meetings.SportCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_sport_profiles',
    )

    # Геолокация
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    find_area = models.FloatField(null=True, blank=True)  # радиус поиска?

    # Дата рождения
    birthday = models.DateTimeField(null=True, blank=True)

    # 🔥 Telegram ID (уникальный)
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        help_text="Telegram user ID (получается из виджета)"
    )

    # Списки — теперь через M2M (не JSON!)
    meetings = models.ManyToManyField('sf_meetings.Meeting', related_name='profiles', blank=True)
    sport_categories = models.ManyToManyField(
        'sf_meetings.SportCategory', 
        related_name='interested_profiles', 
        blank=True)

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

