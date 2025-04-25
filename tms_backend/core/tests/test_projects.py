from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Project, User
from rest_framework.authtoken.models import Token

class ProjectTests(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.manager_user = User.objects.create_user(username='manager', password='password', role='Project Manager')
        self.regular_user = User.objects.create_user(username='user', password='password', role='Client')

        # Create tokens for each user
        self.admin_token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.manager_token, _ = Token.objects.get_or_create(user=self.manager_user)
        self.regular_user_token, _ = Token.objects.get_or_create(user=self.regular_user)

        # Test project data
        self.project_data = {'name': 'Test Project', 'description': 'A project for testing.'}

    # Test creation of a project as an admin
    def test_create_project_as_admin(self):
        response = self.client.post('/api/projects/', self.project_data, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test creation of a project as a regular user (should fail)
    def test_create_project_as_regular_user(self):
        response = self.client.post('/api/projects/', self.project_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token.key}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test getting the project list (admin user)
    def test_get_project_list(self):
        response = self.client.get('/api/projects/', HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test updating a project as admin
    def test_update_project_as_admin(self):
        project = Project.objects.create(**self.project_data)
        update_data = {'name': 'Updated Project'}
        response = self.client.put(f'/api/projects/{project.id}/', update_data, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Project')

    # Test updating a project as a manager (should be allowed if manager)
    def test_update_project_as_manager(self):
        project = Project.objects.create(**self.project_data)
        update_data = {'name': 'Updated by manager'}
        response = self.client.put(f'/api/projects/{project.id}/', update_data, HTTP_AUTHORIZATION=f'Token {self.manager_token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated by manager')

    # Test deleting a project as manager
    def test_delete_project_as_manager(self):
        project = Project.objects.create(**self.project_data)
        response = self.client.delete(f'/api/projects/{project.id}/', HTTP_AUTHORIZATION=f'Token {self.manager_token.key}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test deleting a project as a regular user (should fail)
    def test_delete_project_as_regular_user(self):
        project = Project.objects.create(**self.project_data)
        response = self.client.delete(f'/api/projects/{project.id}/', HTTP_AUTHORIZATION=f'Token {self.regular_user_token.key}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test project creation with missing name field (should fail)
    def test_create_project_missing_name(self):
        data = {'description': 'Missing project name.'}
        response = self.client.post('/api/projects/', data, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test project creation with missing description field (should fail)
    def test_create_project_missing_description(self):
        data = {'name': 'Project without description'}
        response = self.client.post('/api/projects/', data, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test that only admins can delete a project (as an edge case)
    def test_delete_project_as_admin(self):
        project = Project.objects.create(**self.project_data)
        response = self.client.delete(f'/api/projects/{project.id}/', HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test project creation with trailing slash (ensuring proper URL format)
    def test_create_project_with_trailing_slash(self):
        response = self.client.post('/api/projects/', self.project_data, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
