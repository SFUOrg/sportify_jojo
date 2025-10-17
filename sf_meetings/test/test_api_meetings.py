from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from sf_meetings.models import Meeting, SportCategory
from datetime import timedelta
import json


class MeetingAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.sport_category = SportCategory.objects.create(name='Football', description='Football games')
        
        # Create some test meetings
        self.future_date = timezone.now() + timedelta(days=1)
        self.past_date = timezone.now() - timedelta(days=1)
        
        self.meeting1 = Meeting.objects.create(
            title='Test Meeting 1',
            description='Test Description 1',
            latitude=55.7558,
            longitude=37.6176,
            date_time=self.future_date,
            organizer=self.user,
            sport_category=self.sport_category
        )
        
        self.meeting2 = Meeting.objects.create(
            title='Test Meeting 2',
            description='Test Description 2',
            latitude=55.7558,
            longitude=37.6176,
            date_time=self.future_date + timedelta(hours=2),
            organizer=self.user,
            sport_category=self.sport_category
        )
        
        # Create another user and meeting
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.other_meeting = Meeting.objects.create(
            title='Other Meeting',
            description='Other Description',
            latitude=55.7558,
            longitude=37.6176,
            date_time=self.future_date + timedelta(hours=4),
            organizer=self.other_user,
            sport_category=self.sport_category
        )

    def test_list_meetings_api_authenticated(self):
        """Test that authenticated users can list meetings"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('api_list_meetings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)  # All meetings should be returned

    def test_list_meetings_api_unauthenticated(self):
        """Test that unauthenticated users cannot access the meeting list"""
        response = self.client.get(reverse('api_list_meetings'))
        self.assertEqual(response.status_code, 401)  # Should be unauthorized

    def test_list_meetings_with_filters(self):
        """Test filtering meetings by sport category"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('api_list_meetings'), {'sport_category': self.sport_category.id})
        self.assertEqual(response.status_code, 200)
        # Should return meetings with the specified sport category
        self.assertEqual(len(response.json()), 3)

    def test_list_meetings_by_user_participation(self):
        """Test filtering meetings by user participation"""
        # Add user to other meeting as a participant
        self.other_meeting.participants.add(self.user)
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('api_list_meetings'), {'joined': 'true'})
        self.assertEqual(response.status_code, 200)
        # Should return meetings the user participates in (includes meetings they organized)
        self.assertGreaterEqual(len(response.json()), 2)

    def test_list_meetings_by_user_organization(self):
        """Test filtering meetings by user organization"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('api_list_meetings'), {'organized': 'true'})
        self.assertEqual(response.status_code, 200)
        # Should return meetings organized by this user only
        self.assertEqual(len(response.json()), 2)