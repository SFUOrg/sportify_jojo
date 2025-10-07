# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Meeting(models.Model):
    title = models.CharField(max_length=255, help_text="Название встречи")
    description = models.TextField(blank=True, help_text="Описание встречи")

    # 📍 Геолокация встречи
    latitude = models.FloatField(
        help_text="Широта места проведения встречи"
    )
    longitude = models.FloatField(
        help_text="Долгота места проведения встречи"
    )

    # 📅 Время и дата
    date_time = models.DateTimeField(help_text="Дата и время начала встречи")

    # 👤 Организатор (админ встречи)
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # если пользователь удалён — удаляем и встречу
        related_name='organized_meetings',
        help_text="Пользователь, создавший встречу"
    )

    # 🧑‍🤝‍🧑 Участники (M2M через Profile или напрямую через User)
    participants = models.ManyToManyField(
        User,
        related_name='participating_meetings',
        blank=True,
        help_text="Участники встречи"
    )

    # 🏷️ Категория спорта (опционально, если нужно)
    sport_category = models.ForeignKey(
        'SportCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meetings',
        help_text="Категория спорта для этой встречи"
    )

    # 📌 Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date_time.strftime('%d.%m.%Y %H:%M')})"

    def save(self, *args, **kwargs):
        # Проверяем, является ли это новой записью
        is_new_meeting = self.pk is None

        # Вызываем родительский метод save() для сохранения объекта
        super().save(*args, **kwargs)

        # Если это новая встреча и у неё есть организатор
        if is_new_meeting and self.organizer:
            # Добавляем организатора в список участников
            # add() автоматически избегает дубликатов
            self.participants.add(self.organizer)

    class Meta:
        ordering = ['date_time']
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"