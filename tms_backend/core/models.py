from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Define the possible roles as choices
    ADMIN = 'Admin'
    PROJECT_MANAGER = 'Project Manager'
    PROJECT_LEAD = 'Project Lead'
    DEVELOPER = 'Developer'
    CLIENT = 'Client'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PROJECT_MANAGER, 'Project Manager'),
        (PROJECT_LEAD, 'Project Lead'),
        (DEVELOPER, 'Developer'),
        (CLIENT, 'Client'),
    ]

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=DEVELOPER
    )

    def __str__(self):
        return self.username

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('User', related_name='projects')  # Tagged users
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_creators')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_authors')  # or just 'user_comments'
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_creators')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.task.title}"

