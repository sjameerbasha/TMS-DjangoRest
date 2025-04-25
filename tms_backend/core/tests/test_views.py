from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import User, Project, Task, Comment

class ViewsTestCase(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.admin = User.objects.create_user(username='admin', password='admin123', role='Admin')
        self.pm = User.objects.create_user(username='pm', password='pm123', role='Project Manager')
        self.dev = User.objects.create_user(username='dev', password='dev123', role='Developer')
        self.client_user = User.objects.create_user(username='client', password='client123', role='Client')

        # Create a project, task, and comment
        self.project = Project.objects.create(name='Project A', description='Test project', created_by=self.admin)
        self.task = Task.objects.create(title='Task A', project=self.project, status='Open', created_by=self.admin)
        self.comment = Comment.objects.create(content='Initial comment', task=self.task, project=self.project, user=self.admin, created_by=self.admin)

        self.client = APIClient()

    def login(self, user):
        self.client.force_authenticate(user=user)

    def test_register(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "password2": "newpass123",
            "email": "new@site.com",
            "role": "Client",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_profile_view_authenticated(self):
        self.login(self.admin)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_view_unauthenticated(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_list_users(self):
        self.login(self.admin)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pm_can_create_project(self):
        self.login(self.pm)
        url = reverse('project-list')
        data = {"name": "New Project", "description": "PM test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_create_project(self):
        self.login(self.client_user)
        url = reverse('project-list')
        data = {"name": "Forbidden", "description": "Client shouldn't create"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_create_task(self):
        self.login(self.client_user)
        url = reverse('task-list')
        data = {
            "title": "Client task",
            "status": "Open",
            "project": self.project.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_comment(self):
        self.login(self.dev)
        url = reverse('comment-list')
        data = {
            "content": "New comment",
            "task": self.task.id,
            "project": self.project.id  # Add the project ID here
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_can_comment(self):
        self.login(self.client_user)
        url = reverse('comment-list')
        data = {
            "content": "Client shouldn't comment",
            "task": self.task.id,
            "project": self.project.id  # Add the project ID here
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
