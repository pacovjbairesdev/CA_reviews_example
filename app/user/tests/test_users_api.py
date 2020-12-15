from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Function for typing less"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the functionality available for an
       unauthenticated user"""

    def setUp(self):
        self.client = APIClient()

# Tests for checking validations and create functionality
    def test_create_valid_user_with_the_api(self):
        """Test creating user with the API.
           Also checking the password not visible in request"""
        payload = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_duplicated_user(self):
        """Test for duplicated user validation"""
        payload = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length(self):
        """Test password is valid (more than 6 characters)"""
        payload = {
            'email': 'test@test.com',
            'password': '1234',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exist)

# Tests for checking token validation
    def test_create_token_for_user(self):
        """"Test that a token can be created for the user"""
        payload = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_creation(self):
        """Test that token is not created if invalid
           credentials are given"""
        payload1 = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        payload2 = {
            'email': 'test@test.com',
            'password': 'wrong password',
            'name': 'Test Name'
        }
        create_user(**payload1)
        res = self.client.post(TOKEN_URL, payload2)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload1 = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        payload2 = {
            'email': 'user2@test.com',
            'password': 'other password',
            'name': 'Test Name'
        }
        create_user(**payload1)
        res = self.client.post(TOKEN_URL, payload2)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Check that email and pass are required"""
        payload1 = {
            'email': 'test@test.com',
            'password': '',
            'name': 'Test Name'
        }
        payload2 = {
            'email': '',
            'password': 'other password',
            'name': 'Test Name'
        }
        res = self.client.post(TOKEN_URL, payload1)#Checking for password

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post(TOKEN_URL, payload2)#Checking for email

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# Test for security of the updating profile view
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for accessing
           the user:me viewpoint"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require user authentication"""

    def setUp(self):
        payload = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'Test Name'
        }
        self.user = create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test accesing the user:me viewpoint for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the user:me viewpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating an authenticated user profile
           in the user:me viewpoint"""
        payload = {
            'password': 'New 123456',
            'name': 'New Test Name'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
