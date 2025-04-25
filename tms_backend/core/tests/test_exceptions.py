from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from core.exceptions import UserView
from core.models import User
from rest_framework import status
from core.serializers import UserSerializer

class CustomExceptionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_user_not_found_exception(self):
        view = UserView.as_view()
        request = self.factory.get('/users/999/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_post_user_missing_fields(self):
        view = UserView.as_view()
        request = self.factory.post('/users/', {}, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_post_user_success(self):
        view = UserView.as_view()
        request = self.factory.post('/users/', {'username': 'newuser', 'password': 'pass123'}, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user_not_found(self):
        view = UserView.as_view()
        request = self.factory.delete('/users/999/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_inactive_unauthorized(self):
        inactive_user = User.objects.create_user(username='inactiveuser', password='testpass', is_active=False)
        view = UserView.as_view()
        request = self.factory.delete(f'/users/{inactive_user.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=inactive_user.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_success(self):
        view = UserView.as_view()
        request = self.factory.delete(f'/users/{self.user.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validate_username_already_exists(self):
        serializer = UserSerializer(data={'username': 'testuser', 'password': 'testpass'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_validate_username_unique(self):
        serializer = UserSerializer(data={'username': 'uniqueuser', 'password': 'testpass'})
        self.assertTrue(serializer.is_valid())
