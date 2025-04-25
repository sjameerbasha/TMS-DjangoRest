from rest_framework import permissions

class IsAdminOrProjectManager(permissions.BasePermission):
    """
    Permission to allow only Admins or Project Managers to view or delete users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, OPTIONS, HEAD to everyone
        return request.user.is_authenticated and request.user.role in ['Admin', 'Project Manager']


class CanCreateEditDeleteProjects(permissions.BasePermission):
    """
    - Allow read-only (GET, OPTIONS, HEAD) to everyone.
    - Allow create/edit/delete (POST, PUT, PATCH, DELETE) only to Admin and Project Manager.
    - Regular users (Client) can only view (GET).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only (GET, OPTIONS, HEAD) to everyone
        
        # Allow create/edit/delete for Admin and Project Manager only, restrict for Clients
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return request.user.is_authenticated and request.user.role in ['Admin', 'Project Manager']
        
        # Block clients from creating or editing projects
        return request.user.is_authenticated and request.user.role in ['Admin', 'Project Manager']


class CanCreateTasks(permissions.BasePermission):
    """
    Permission to allow all users except clients to create tasks.
    Clients cannot create tasks or delete them.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Clients cannot create or delete tasks
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.role != 'Client'
        if request.method == 'DELETE':
            return request.user.is_authenticated and request.user.role != 'Client'
        return request.user.is_authenticated
    
    
class CanComment(permissions.BasePermission):
    """
    Permission to allow all authenticated users to create, update, delete, and view comments.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users to perform any action (POST, PUT, DELETE, GET)
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, OPTIONS, HEAD to everyone
        
        # Allow all authenticated users to create, update, or delete comments
        return request.user.is_authenticated


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access (GET, OPTIONS, HEAD) to everyone.
    Authenticated users can perform write actions depending on their role.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only (GET, OPTIONS, HEAD) to everyone
        return request.user.is_authenticated
