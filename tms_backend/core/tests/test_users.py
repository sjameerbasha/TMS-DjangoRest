from rest_framework.test import APITestCase
from rest_framework import status
from core.models import User
from rest_framework.authtoken.models import Token

class UserTests(APITestCase):

    def setUp(self):
        self.strong_password = 'S3cur3P@ssword!'  # Avoid 'password123'

        # Standard test user data for registration
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': self.strong_password,
            'password2': self.strong_password,
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'Client'
        }

        # Create an existing user
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password=self.strong_password,
            first_name='Existing',
            last_name='User',
            role='Project Manager'
        )
        Token.objects.get_or_create(user=self.existing_user)

    def tearDown(self):
        Token.objects.all().delete()
        User.objects.all().delete()

    def test_user_registration(self):
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        user = User.objects.get(username='testuser')
        token_count = Token.objects.filter(user=user).count()
        self.assertEqual(token_count, 1)

    def test_user_registration_with_existing_username(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'existinguser',
            'email': 'duplicate@example.com',
            'password': self.strong_password,
            'password2': self.strong_password,
            'first_name': 'Dup',
            'last_name': 'User',
            'role': 'Project Manager'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        self.client.post('/api/auth/register/', self.user_data)

        login_data = {
            'username': 'testuser',
            'password': self.strong_password
        }
        response = self.client.post('/api/auth/login/', login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        user = User.objects.get(username='testuser')
        token_count = Token.objects.filter(user=user).count()
        self.assertEqual(token_count, 1)

    def test_token_creation_after_registration(self):
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testuser')
        token = Token.objects.get(user=user)
        self.assertIsNotNone(token)
