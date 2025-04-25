from rest_framework.test import APITestCase, APIClient
from core.models import User, Task, Project, Comment
from rest_framework.authtoken.models import Token

class CommentTests(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.user = User.objects.create_user(username="commenter", password="1234", role="Developer")
        self.admin_user = User.objects.create_user(username="admin", password="1234", role="Admin")
        self.project = Project.objects.create(name="P", description="D")
        self.task = Task.objects.create(
            title="T", description="D", status="To Do",
            assigned_to=self.user, project=self.project,
            created_by=self.user
        )
        self.token = Token.objects.get(user=self.user)
        self.admin_token = Token.objects.get(user=self.admin_user)

        self.client = APIClient()

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/api/comments/", {
            "content": "New comment",
            "task": self.task.id,
            "project": self.project.id
        })
        self.assertEqual(response.status_code, 201)

    def test_get_comment(self):
        comment = Comment.objects.create(
            content="Test", task=self.task, project=self.project,
            user=self.user, created_by=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f"/api/comments/{comment.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_comment(self):
        comment = Comment.objects.create(
            content="Old", task=self.task, project=self.project,
            user=self.user, created_by=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(f"/api/comments/{comment.id}/", {
            "content": "Updated",
            "task": self.task.id,
            "project": self.project.id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_comment(self):
        comment = Comment.objects.create(
            content="Del", task=self.task, project=self.project,
            user=self.user, created_by=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f"/api/comments/{comment.id}/")
        self.assertEqual(response.status_code, 204)

