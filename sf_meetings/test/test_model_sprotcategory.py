from django.test import TestCase
from sf_meetings.models import SportCategory
from django.core.exceptions import ValidationError

class SportCategoryModelTest(TestCase):

    def test_sport_category_creation(self):
        """Тест: создание категории спорта с обязательными полями"""
        category = SportCategory.objects.create(
            name="Бег",
            description="Бег на свежем воздухе"
        )
        self.assertEqual(category.name, "Бег")
        self.assertEqual(category.description, "Бег на свежем воздухе")

    def test_sport_category_str_method(self):
        """Тест: метод __str__ возвращает имя категории"""
        category = SportCategory.objects.create(name="Футбол")
        self.assertEqual(str(category), "Футбол")

    def test_sport_category_name_is_unique(self):
        """Тест: имя категории должно быть уникальным"""
        SportCategory.objects.create(name="Плавание")

        with self.assertRaises(Exception):  # вызовет IntegrityError
            SportCategory.objects.create(name="Плавание")

    def test_sport_category_name_max_length(self):
        long_name = "A" * 101
        category = SportCategory(name=long_name)
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_sport_category_description_optional(self):
        """Тест: описание может быть пустым"""
        category = SportCategory.objects.create(name="Йога")
        self.assertEqual(category.description, "")
        # или None, если в модели стоит null=True — но у тебя blank=True, null=False по умолчанию
        # так что будет пустая строка