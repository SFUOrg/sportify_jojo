# myapp/management/commands/generate_meetings.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from  sf_meetings.models import Meeting 
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Создаёт 10 тестовых встреч в Москве'

    def handle(self, *args, **options):
        # Найдём или создадим тестового пользователя (организатора)
        # Для простоты, возьмём первого пользователя или создадим тестового
        test_user, created = User.objects.get_or_create(
            username='test_organizer',
            defaults={'email': 'test@example.com', 'password': 'pbkdf2_sha256$...'} # Пароль можно не указывать или захешировать
        )
        if created:
            # Установим простой пароль для тестового пользователя, если он создан
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS(f'Создан тестовый организатор: {test_user.username} (пароль: testpass123)'))

        # Координаты центра Москвы (примерные)
        moscow_center_lat = 55.7558
        moscow_center_lng = 37.6176

        # Диапазон (в градусах) для случайного смещения (~2-3 км в каждую сторону)
        lat_range = 0.02
        lng_range = 0.02

        for i in range(10):
            # Случайные координаты рядом с центром Москвы
            lat = moscow_center_lat + random.uniform(-lat_range, lat_range)
            lng = moscow_center_lng + random.uniform(-lng_range, lng_range)

            # Случайная дата в ближайшие 7 дней
            future_date = datetime.now() + timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59))

            meeting = Meeting.objects.create(
                title=f'Тестовая встреча {i+1}',
                description=f'Описание для тестовой встречи номер {i+1}.',
                latitude=lat,
                longitude=lng,
                date_time=future_date,
                organizer=test_user,
                # sport_category можно оставить пустым или создать и присвоить
            )
            self.stdout.write(self.style.SUCCESS(f'Создана встреча: {meeting.title}'))

        self.stdout.write(self.style.SUCCESS('Генерация тестовых встреч завершена.'))