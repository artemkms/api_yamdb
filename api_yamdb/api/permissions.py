
from rest_framework import permissions


class SuperOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or (
            request.user.role == 'admin') or (
            request.method in permissions.SAFE_METHODS
        )
