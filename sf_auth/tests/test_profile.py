from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
import uuid

from sf_auth.models import Profile
from sf_meetings.models import Meeting, SportCategory


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.sport_category = SportCategory.objects.create(name="Бег")
        self.meeting = Meeting.objects.create(
            title="Утренний бег",
            date_time="2025-06-01T07:00:00Z",
            latitude=55.7558,
            longitude=37.6176,
            organizer=self.user
        )

    def test_profile_creation_generates_uuid(self):
        """Тест: UUID генерируется автоматически и является уникальным"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertIsInstance(profile.uuid, uuid.UUID)
        self.assertIsNotNone(profile.uuid)

    def test_profile_str_method(self):
        """Тест: метод __str__ возвращает ожидаемую строку"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertEqual(str(profile), f"Profile of {self.user.username}")

    def test_profile_one_to_one_with_user(self):
        """Тест: связь OneToOne с User работает в обе стороны"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(self.user.profile, profile)

    def test_telegram_id_is_unique(self):
        """Тест: telegram_id должен быть уникальным"""
        telegram_id = 123456789
        profile1, created = Profile.objects.get_or_create(user=self.user)
        profile1.telegram_id = telegram_id
        profile1.save()

        user2 = User.objects.create_user(username='user2', password='pass')
        # Create profile for second user with same telegram_id, this should fail due to uniqueness
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=user2, telegram_id=telegram_id)

    def test_telegram_id_can_be_null(self):
        """Тест: telegram_id может быть пустым"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertIsNone(profile.telegram_id)

    def test_profile_photo_field(self):
        """Тест: можно сохранить изображение в profile_photo"""
        mock_image = SimpleUploadedFile(
            name='avatar.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.profile_photo = mock_image
        profile.save()
        self.assertTrue(profile.profile_photo.name.startswith('profile_photos/avatar'))

    def test_geolocation_fields(self):
        """Тест: поля геолокации сохраняются корректно"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.latitude = 55.7558
        profile.longitude = 37.6176
        profile.find_area = 5.5  # км
        profile.save()
        self.assertEqual(profile.latitude, 55.7558)
        self.assertEqual(profile.longitude, 37.6176)
        self.assertEqual(profile.find_area, 5.5)

    def test_main_sport_foreign_key(self):
        """Тест: основной вид спорта (main_sport) работает"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.main_sport = self.sport_category
        profile.save()
        self.assertEqual(profile.main_sport, self.sport_category)
        # Проверяем обратную связь (related_name='main_sport_profiles')
        self.assertIn(profile, self.sport_category.main_sport_profiles.all())

    def test_sport_categories_m2m(self):
        """Тест: M2M связь с категориями спорта работает"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.sport_categories.add(self.sport_category)

        self.assertIn(self.sport_category, profile.sport_categories.all())
        # Проверяем обратную связь (related_name='interested_profiles')
        self.assertIn(profile, self.sport_category.interested_profiles.all())

    def test_meetings_m2m(self):
        """Тест: M2M связь с встречами работает"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.meetings.add(self.meeting)

        self.assertIn(self.meeting, profile.meetings.all())
        self.assertIn(profile, self.meeting.profiles.all())

    def test_created_at_and_updated_at_auto_set(self):
        """Тест: created_at и updated_at устанавливаются автоматически"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
        self.assertLessEqual(profile.created_at, profile.updated_at)

    def test_uuid_is_immutable(self):
        """Тест: UUID не меняется после обновления профиля"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        original_uuid = profile.uuid

        profile.second_name = "Новое имя"
        profile.save()
        profile.refresh_from_db()

        self.assertEqual(profile.uuid, original_uuid)

