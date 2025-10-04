from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from sf_meetings.models import Meeting, SportCategory
from datetime import datetime, timezone


class MeetingModelTest(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='password123'
        )
        self.participant = User.objects.create_user(
            username='participant',
            password='password123'
        )
        self.sport_category = SportCategory.objects.create(
            name="Бег",
            description="Утренние пробежки"
        )

    def test_meeting_creation_required_fields(self):
        """Тест: создание встречи с обязательными полями"""
        meeting = Meeting.objects.create(
            title="Утренняя пробежка",
            date_time=datetime(2025, 6, 1, 8, 0, tzinfo=timezone.utc),
            latitude=55.7558,
            longitude=37.6176,
            organizer=self.organizer
        )
        self.assertEqual(meeting.title, "Утренняя пробежка")
        self.assertEqual(meeting.organizer, self.organizer)
        self.assertEqual(meeting.latitude, 55.7558)
        self.assertEqual(meeting.longitude, 37.6176)
        self.assertIsNotNone(meeting.created_at)
        self.assertIsNotNone(meeting.updated_at)

    def test_meeting_str_method(self):
        """Тест: метод __str__ возвращает ожидаемую строку"""
        meeting = Meeting.objects.create(
            title="Йога в парке",
            date_time=datetime(2025, 6, 5, 18, 0, tzinfo=timezone.utc),
            latitude=59.9343,
            longitude=30.3351,
            organizer=self.organizer
        )
        expected = "Йога в парке (05.06.2025 18:00)"
        self.assertEqual(str(meeting), expected)

    def test_meeting_with_optional_fields(self):
        """Тест: встреча с описанием и категорией спорта"""
        meeting = Meeting.objects.create(
            title="Футбол",
            description="Играем на стадионе",
            date_time=datetime(2025, 7, 10, 19, 0, tzinfo=timezone.utc),
            latitude=50.4501,
            longitude=30.5234,
            organizer=self.organizer,
            sport_category=self.sport_category
        )
        self.assertEqual(meeting.description, "Играем на стадионе")
        self.assertEqual(meeting.sport_category, self.sport_category)

    def test_meeting_participants_m2m(self):
        """Тест: связь M2M с участниками работает"""
        meeting = Meeting.objects.create(
            title="Велопрогулка",
            date_time=datetime(2025, 8, 1, 10, 0, tzinfo=timezone.utc),
            latitude=55.0,
            longitude=37.0,
            organizer=self.organizer
        )
        meeting.participants.add(self.participant)

        self.assertIn(self.participant, meeting.participants.all())
        self.assertIn(meeting, self.participant.participating_meetings.all())

    def test_meeting_organizer_is_required(self):
        """Тест: organizer — обязательное поле (не может быть null)"""
        with self.assertRaises(Exception):  # IntegrityError
            Meeting.objects.create(
                title="Без организатора",
                date_time=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
                latitude=0.0,
                longitude=0.0,
                # organizer не указан → ошибка
            )

    def test_meeting_latitude_longitude_required(self):
        """Тест: latitude и longitude обязательны"""
        with self.assertRaises(Exception):
            Meeting.objects.create(
                title="Без координат",
                date_time=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
                organizer=self.organizer,
                # latitude и longitude не указаны
            )

    def test_meeting_ordering(self):
        """Тест: встречи сортируются по дате (Meta.ordering)"""
        meeting1 = Meeting.objects.create(
            title="Ранняя",
            date_time=datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc),
            latitude=55.0,
            longitude=37.0,
            organizer=self.organizer
        )
        meeting2 = Meeting.objects.create(
            title="Поздняя",
            date_time=datetime(2025, 1, 2, 8, 0, tzinfo=timezone.utc),
            latitude=55.0,
            longitude=37.0,
            organizer=self.organizer
        )
        meetings = Meeting.objects.all()
        self.assertEqual(meetings[0], meeting1)
        self.assertEqual(meetings[1], meeting2)

    def test_meeting_sport_category_can_be_null(self):
        """Тест: sport_category может отсутствовать"""
        meeting = Meeting.objects.create(
            title="Свободная тренировка",
            date_time=datetime(2025, 9, 1, 17, 0, tzinfo=timezone.utc),
            latitude=55.0,
            longitude=37.0,
            organizer=self.organizer
            # sport_category не указан — OK
        )
        self.assertIsNone(meeting.sport_category)