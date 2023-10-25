# users/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser, Player
from .forms import CustomUserCreationForm
from .views import SignupPageView


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
        username='will',
        email='will@email.com',
        password='testpass123'
        )

        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
        username='superadmin',
        email='superadmin@email.com',
        password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class SignupPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
        self.response, 'Hi there! I should not be on the page.')



    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class PlayerModelTest(TestCase):
    
    def setUp(self):
        # Create a user if it doesn't exist, or get an existing user
        self.user, created = CustomUser.objects.get_or_create(username='testuser', email='test@example.com', password='testpassword')
        self.player = Player.objects.create(user=self.user, name='Test Player', handicap=10)

    def tearDown(self):
        # Clean up after each test by deleting the player and user
        self.player.delete()
        self.user.delete()

    def test_player_str(self):
        self.assertEqual(str(self.player), 'Test Player')

    def test_player_absolute_url(self):
        url = self.player.get_absolute_url()
        expected_url = reverse('users:profile')
        self.assertEqual(url, expected_url)

    def test_player_creation(self):
        self.assertTrue(Player.objects.filter(user=self.user, name='Test Player', handicap=10).exists())

    def test_player_profile_picture_upload(self):
        profile_picture = SimpleUploadedFile("profile_picture.jpg", b"file_content", content_type="image/jpeg")
        self.player.profile_picture = profile_picture
        self.player.save()

        self.assertTrue(self.player.profile_picture)