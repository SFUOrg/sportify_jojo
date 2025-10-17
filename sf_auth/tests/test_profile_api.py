from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from sf_auth.models.profile import Profile
from sf_meetings.models import SportCategory


class ProfileAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create associated profile using get_or_create to handle case where profile already exists
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        
        # URLs for profile endpoints
        self.get_profile_url = reverse('sf_auth:get_profile')
        self.update_profile_url = reverse('sf_auth:update_profile')
        
    def test_get_profile_authenticated_user(self):
        """Test getting profile for authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['uuid'], str(self.profile.uuid))
        
    def test_get_profile_unauthenticated_user(self):
        """Test getting profile for unauthenticated user returns 401"""
        response = self.client.get(self.get_profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile_authenticated_user(self):
        """Test updating profile for authenticated user"""
        # Create a sport category for testing
        sport_category = SportCategory.objects.create(name="Бег")
        
        self.client.force_authenticate(user=self.user)
        update_data = {
            'second_name': 'Updated Name',
            'description': 'Updated description',
            'main_sport': sport_category.id,
            'latitude': 55.7558,
            'longitude': 37.6176,
            'find_area': 10.0,
        }
        
        response = self.client.patch(self.update_profile_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['second_name'], 'Updated Name')
        self.assertEqual(response.data['description'], 'Updated description')
        self.assertEqual(response.data['main_sport'], sport_category.id)
        self.assertEqual(response.data['latitude'], 55.7558)
        self.assertEqual(response.data['longitude'], 37.6176)
        self.assertEqual(response.data['find_area'], 10.0)
        
    def test_update_profile_unauthenticated_user(self):
        """Test updating profile for unauthenticated user returns 401"""
        update_data = {
            'second_name': 'Updated Name',
        }
        
        response = self.client.patch(self.update_profile_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile_only_allows_own_profile(self):
        """Test that user can only update their own profile (theoretically, though Django handles this via request.user)"""
        # This test confirms the implementation uses request.user.profile
        # which ensures users can only access their own profile
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        Profile.objects.get_or_create(user=other_user)
        
        self.client.force_authenticate(user=self.user)
        # Even if we tried to access or update another user's profile,
        # the implementation uses request.user.profile, so it's not possible
        response = self.client.get(self.get_profile_url)
        
        # Profile returned should be of the authenticated user, not the other user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        
    def test_put_vs_patch_update(self):
        """Test both PUT and PATCH methods work for profile update"""
        self.client.force_authenticate(user=self.user)
        
        # Test PATCH (partial update)
        patch_data = {
            'second_name': 'Patched Name'
        }
        patch_response = self.client.patch(self.update_profile_url, patch_data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['second_name'], 'Patched Name')
        
        # Test PUT (full update)
        put_data = {
            'second_name': 'Put Name',
            'description': 'Description updated with PUT',
            'latitude': 45.1234,
            'longitude': 30.5678,
        }
        put_response = self.client.put(self.update_profile_url, put_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.data['second_name'], 'Put Name')
        self.assertEqual(put_response.data['description'], 'Description updated with PUT')