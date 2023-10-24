from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse  # Import the reverse function

class UserRegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
        }

    def test_user_registration(self):
        url = reverse('users:user-registration')  # Use the reverse function with the URL name
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_user_registration_with_invalid_data(self):
        url = reverse('users:user-registration')  # Use the reverse function with the URL name
        invalid_data = {'username': '', 'email': 'invalid-email', 'password': 'short'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate(self):
        url = reverse('users:user-registration')  # Use the reverse function with the URL name
        response1 = self.client.post(url, self.user_data, format='json')
        response2 = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)