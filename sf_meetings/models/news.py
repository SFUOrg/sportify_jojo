# sf_meetings/models.py - добавьте это к существующим моделям
from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Заголовок новости"
    )   
    content = models.TextField(
        help_text="Содержание новости"
    )
    # Фото новости (опционально)
    image = models.ImageField(
        upload_to='news_photos/',
        blank=True,
        null=True,
        help_text="Изображение для новости"
    )
    # Связь с встречей 
    meeting = models.ForeignKey(
        'Meeting',
        on_delete=models.CASCADE,
        related_name='news',
        null=True,
        help_text="Связанная встреча (если применимо)"
    )
    
    # Автор новости
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_news',
        help_text="Автор новости"
    )
    
    # Просмотры пользователей
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Количество просмотров новости"
    )
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Опубликована ли новость"
    )
    
    def __str__(self):
        return f"{self.title} (автор: {self.author.username}, просмотры: {self.views_count})"
    
    def increment_views(self):
        """Увеличивает счетчик просмотров на 1"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_views_count(self):
        """Возвращает количество просмотров"""
        return self.views_count
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"