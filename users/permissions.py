from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin' or request.user.is_staff))


class IsModerator(permissions.BasePermission):
    """Права доступа для модератора"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')
