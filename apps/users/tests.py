# users/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser, Player
from .forms import CustomUserCreationForm
from .views import SignupPageView
from django.core.cache import cache

class login:
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success, f"login with username={user!r}, password={password!r} failed"
        )

    def __enter__(self):
        passclear

    def __exit__(self, *args):
        self.testcase.client.logout()


class BaseTestCase(TestCase):
    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = "test"
        self.user_bob = self.create_user("bob", "bob@bob.com", self.user_pw)
        self.user_steve = self.create_user("steve", "steve@steve.com", self.user_pw)
        self.user_susan = self.create_user("susan", "susan@susan.com", self.user_pw)
        self.user_amy = self.create_user("amy", "amy@amy.amy.com", self.user_pw)
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, email_address, password):
        user = CustomUser.objects.create_user(username, email_address, password)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)

class SignupPageTests(BaseTestCase):
    def test_signup_template(self):
        url = reverse('account_signup')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        self.assertContains(response, 'Sign Up')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user('testusername', 'testemail@example.com')  # Create a new user
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, 'testusername')
        self.assertEqual(get_user_model().objects.all()[0].email, 'testemail@example.com')


class PlayerModelTest(BaseTestCase):   
    def setUp(self):
        super().setUp()  # Call the setUp method of the base class
        # Reference the users created in the base class
        self.user = self.user_bob  # Replace 'user_bob' with the actual user you want to use
        self.player = Player.objects.create(user=self.user, name='Test Player', handicap=10)

    def tearDown(self):
        # Clean up after each test by deleting the player
        self.player.delete()
        super().tearDown()  # Call the tearDown method of the base class

    def test_player_str(self):
        self.assertEqual(str(self.player), 'Test Player')

    def test_player_absolute_url(self):
        with self.login(self.user.username, self.user_pw):  # Use the user's username and password from the base class
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