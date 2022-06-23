from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'admin'


class IsRoleModerator(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'moderator'
