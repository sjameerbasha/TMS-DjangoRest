from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from core.utils.notifications import send_task_assignment_email

from .models import User, Project, Task, Comment
from .serializers import (
    UserSerializer, ProjectSerializer, TaskSerializer, CommentSerializer,
    RegisterSerializer, ProfileSerializer
)
from .permissions import IsAdminOrProjectManager, CanCreateEditDeleteProjects, CanCreateTasks, CanComment, IsAuthenticatedOrReadOnly


# ------------------ USER VIEWSET ------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrProjectManager]  # Only admin and project manager can view/delete users


# ------------------ PROJECT VIEWSET + FILTER ------------------
class ProjectFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'description']

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [CanCreateEditDeleteProjects, IsAuthenticatedOrReadOnly]  # Restrict actions to clients and developers for non-read operations
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProjectFilter
    search_fields = ['name', 'description']


# ------------------ TASK VIEWSET + FILTER ------------------
class TaskFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    status = CharFilter(field_name='status', lookup_expr='icontains')
    assigned_to = CharFilter(field_name='assigned_to__username', lookup_expr='icontains')
    project = CharFilter(field_name='project__id', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['title', 'status', 'assigned_to', 'project']


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [CanCreateTasks, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        if task.assigned_to and task.assigned_to.email:
            send_task_assignment_email(
                to_email=task.assigned_to.email,
                task_title=task.title,
                assigned_by=self.request.user.username
            )

    def perform_update(self, serializer):
        old_task = self.get_object()
        new_task = serializer.save()

        if old_task.assigned_to != new_task.assigned_to:
            if new_task.assigned_to and new_task.assigned_to.email:
                send_task_assignment_email(
                    to_email=new_task.assigned_to.email,
                    task_title=new_task.title,
                    assigned_by=self.request.user.username
                )


# ------------------ COMMENT VIEWSET + FILTER ------------------
class CommentFilter(FilterSet):
    content = CharFilter(field_name='content', lookup_expr='icontains')
    task = CharFilter(field_name='task__id', lookup_expr='exact')
    user = CharFilter(field_name='user__id', lookup_expr='exact')
    project = CharFilter(field_name='task__project__id', lookup_expr='exact')

    class Meta:
        model = Comment
        fields = ['content', 'task', 'user', 'project']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CanComment]  # All users can create comments
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CommentFilter
    search_fields = ['content']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, created_by=self.request.user)


# ------------------ REGISTRATION AND PROFILE VIEWS ------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can view their profile

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
