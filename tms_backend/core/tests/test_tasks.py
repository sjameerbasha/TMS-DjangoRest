from rest_framework.test import APITestCase, APIClient
from core.models import User, Task, Project
from rest_framework.authtoken.models import Token

class TaskTests(APITestCase):
    def setUp(self):
        # Create user and project for testing
        self.user = User.objects.create_user(username="dev", password="1234", role="Developer")
        self.project = Project.objects.create(name="Proj", description="Desc")
        
        # Get the token — do NOT create it manually
        self.token = Token.objects.get(user=self.user)

        # Set up client with authentication token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_task(self):
        response = self.client.post("/api/tasks/", {
            "title": "Task 1",
            "description": "Task desc",
            "status": "todo",
            "assigned_to": self.user.id,  # Use user ID for foreign key
            "project": self.project.id,    # Use project ID for foreign key
            "created_by": self.user.id     # Use user ID for created_by field
        })
    
        self.assertEqual(response.status_code, 201)

    def test_update_task(self):
        task = Task.objects.create(
            title="Old Task", description="Old", status="todo",
            assigned_to=self.user, project=self.project, created_by=self.user
        )
        
        response = self.client.put(f"/api/tasks/{task.id}/", {
            "title": "New Task",
            "description": "New",
            "status": "in_progress",
            "assigned_to": self.user.id,  # Use user ID for foreign key
            "project": self.project.id,    # Use project ID for foreign key
            "created_by": self.user.id     # Use user ID for created_by field
        })
        
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        task = Task.objects.create(
            title="Delete Task", description="...", status="todo",
            assigned_to=self.user, project=self.project, created_by=self.user
        )
        
        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, 204)
