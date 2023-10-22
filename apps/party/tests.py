from django.test import TestCase
from django.urls import reverse
from tournaments.models import Tournament
from .forms import PartyForm
from users.models import CustomUser, Player
from .models import Party

class PartyCreateViewTestCase(TestCase):
    def setUp(self):
        # Create a test user and player
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.player = Player.objects.create(user=self.user, name='Test Player', handicap=10)
        
        # Create a test tournament
        self.tournament = Tournament.objects.create(name='Test Tournament', start_date='2023-07-01', end_date='2023-07-05')

    def test_party_create_view_with_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        
        # Get the URL for the Party create view with the tournament ID as a parameter
        url = reverse('party:party_create', kwargs={'tournament_pk': self.tournament.pk})
        
        # Send a GET request to the URL
        response = self.client.get(url)
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the correct template
        self.assertTemplateUsed(response, 'party/party_create.html')
        
        # Check that the form in the response context is a PartyForm instance
        self.assertIsInstance(response.context['form'], PartyForm)
        
        # Check that the form is associated with the correct tournament
        self.assertEqual(response.context['form'].instance.tournament, self.tournament)

    def test_party_create_view_with_unauthenticated_user(self):
        # Get the URL for the Party create view with the tournament ID as a parameter
        url = reverse('party:party_create', kwargs={'tournament_pk': self.tournament.pk})
        
        # Send a GET request to the URL
        response = self.client.get(url)
        
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        
        # Check that the response redirects to the login page
        self.assertRedirects(response, reverse('account_login') + f'?next={url}')

    def test_party_create_view_with_invalid_tournament_id(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        
        # Get a non-existent tournament ID (e.g., -1)
        invalid_tournament_id = -1
        
        # Get the URL for the Party create view with the invalid tournament ID as a parameter
        url = reverse('party:party_create', kwargs={'tournament_pk': invalid_tournament_id})
        
        # Send a GET request to the URL
        response = self.client.get(url)
        
        # Check that the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
