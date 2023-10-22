from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Party, Tournament, Player, Invitation



class InvitationTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name='Test Player')
        self.tournament = Tournament.objects.create(name='Test Tournament')

    def test_create_invitation(self):
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to create an invitation
        response = self.client.post(reverse('tournaments:tournament_invitation', args=[self.tournament.pk]), data={
            'invited_players': [self.user.player.pk],  # Replace this with the player you want to invite
        })

        # Check if the invitation was created and the user is redirected to the tournament detail page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Invitation.objects.filter(tournament=self.tournament, status='pending').exists())


class PartyModelTest(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(name='Test Tournament')
        self.party = Party.objects.create(tournament=self.tournament)

        # Create players
        self.player1 = Player.objects.create(name='Player 1')
        self.player2 = Player.objects.create(name='Player 2')
        self.player3 = Player.objects.create(name='Player 3')

        # Add players to the party
        self.party.players.add(self.player1, self.player2)

    def test_remove_player_from_party(self):
        initial_player_count = self.party.players.count()

        # Remove player from the party
        self.party.remove_player(self.player1)

        # Assert that the player is removed from the party
        self.assertEqual(self.party.players.count(), initial_player_count - 1)
        self.assertNotIn(self.player1, self.party.players.all())

    def test_delete_empty_party(self):
        initial_party_count = Party.objects.count()

        # Remove all players from the party
        self.party.players.clear()

        # Assert that the party is automatically deleted
        self.assertEqual(Party.objects.count(), initial_party_count - 1)
        self.assertFalse(Party.objects.filter(pk=self.party.pk).exists())

    def test_not_delete_non_empty_party(self):
        initial_party_count = Party.objects.count()

        # Attempt to remove a player from the party (without making it empty)
        self.party.remove_player(self.player2)

        # Assert that the party is not deleted
        self.assertEqual(Party.objects.count(), initial_party_count)
        self.assertTrue(Party.objects.filter(pk=self.party.pk).exists())
