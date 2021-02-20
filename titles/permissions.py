from rest_framework import permissions


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        sufficient_conditions = (
            request.method in permissions.SAFE_METHODS,
            obj.author == user,
            user.is_staff,
            user.is_superuser,
        )
        return any(sufficient_conditions)
