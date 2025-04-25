from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser
from core.permissions import (
    IsAdminOrProjectManager,
    CanCreateEditDeleteProjects,
    CanCreateTasks,
    CanComment,
    IsAuthenticatedOrReadOnly
)
from core.models import User

class PermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_user(username='admin', password='admin', role='Admin')
        self.pm = User.objects.create_user(username='pm', password='pm', role='Project Manager')
        self.client_user = User.objects.create_user(username='client', password='client', role='Client')
        self.anon_user = AnonymousUser()  # Use AnonymousUser for unauthenticated user

    def test_is_admin_or_pm_permission(self):
        perm = IsAdminOrProjectManager()

        for method in ['GET', 'OPTIONS', 'HEAD']:
            request = self.factory.generic(method, '/users/')
            request.user = self.anon_user  # Use AnonymousUser here
            self.assertTrue(perm.has_permission(request, None))

        request = self.factory.delete('/users/')
        request.user = self.admin
        self.assertTrue(perm.has_permission(request, None))

        request.user = self.pm
        self.assertTrue(perm.has_permission(request, None))

        request.user = self.client_user
        self.assertFalse(perm.has_permission(request, None))

    def test_can_create_edit_delete_projects(self):
        perm = CanCreateEditDeleteProjects()

        for method in ['GET', 'OPTIONS', 'HEAD']:
            request = self.factory.generic(method, '/projects/')
            request.user = self.anon_user  # Use AnonymousUser here
            self.assertTrue(perm.has_permission(request, None))

        for method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            request = self.factory.generic(method, '/projects/')
            request.user = self.admin
            self.assertTrue(perm.has_permission(request, None))

            request.user = self.pm
            self.assertTrue(perm.has_permission(request, None))

            request.user = self.client_user
            self.assertFalse(perm.has_permission(request, None))

    def test_can_create_tasks(self):
        perm = CanCreateTasks()

        request = self.factory.get('/tasks/')
        request.user = self.anon_user  # Use AnonymousUser here
        self.assertTrue(perm.has_permission(request, None))

        for method in ['POST', 'DELETE']:
            request = self.factory.generic(method, '/tasks/')
            request.user = self.admin
            self.assertTrue(perm.has_permission(request, None))

            request.user = self.pm
            self.assertTrue(perm.has_permission(request, None))

            request.user = self.client_user
            self.assertFalse(perm.has_permission(request, None))

    def test_can_comment(self):
        perm = CanComment()

        for method in ['GET', 'OPTIONS', 'HEAD']:
            request = self.factory.generic(method, '/comments/')
            request.user = self.anon_user  # Use AnonymousUser here
            self.assertTrue(perm.has_permission(request, None))

        for method in ['POST', 'PUT', 'DELETE']:
            request = self.factory.generic(method, '/comments/')
            request.user = self.admin
            self.assertTrue(perm.has_permission(request, None))

            request.user = self.client_user
            self.assertTrue(perm.has_permission(request, None))

    def test_is_authenticated_or_read_only(self):
        perm = IsAuthenticatedOrReadOnly()

        # Simulating unauthenticated request (using AnonymousUser)
        request = self.factory.generic('GET', '/any/')
        request.user = self.anon_user  # Should be AnonymousUser, representing an unauthenticated user
        self.assertTrue(perm.has_permission(request, None))

        for method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Test when user is not authenticated
            request = self.factory.generic(method, '/any/')
            request.user = self.anon_user  # Use AnonymousUser for unauthenticated user
            self.assertFalse(perm.has_permission(request, None))

            # Test when user is authenticated (admin)
            request.user = self.admin
            self.assertTrue(perm.has_permission(request, None))
