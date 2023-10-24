from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class UserRegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
        }

    def test_user_registration(self):
        url = '/api/register/'  # Use the actual URL path
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_user_registration_with_invalid_data(self):
        url = '/api/register/'  # Use the actual URL path
        invalid_data = {'username': '', 'email': 'invalid-email', 'password': 'short'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate(self):
        url = '/api/register/'  # Use the actual URL path
        response1 = self.client.post(url, self.user_data, format='json')
        response2 = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
